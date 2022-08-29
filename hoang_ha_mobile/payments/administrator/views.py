from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt import authentication

from django.core.mail import send_mail
from django.conf import settings

from_mail = settings.EMAIL_HOST_USER

from base.services.notifications.firebase_messaging import Message,FCM
from base.services.stripe.stripe_api import StripeAPI


from hoang_ha_mobile.base.errors import OrderCheckError
from orders.models import Order


# Refund 
class RefundAPI(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        order_id  = request.data['order_id']

        # Check order exists
        order_exist = OrderCheckError.check_order_exists(order_id)
        if order_exist is not None:
            return order_exist
        
        # Check if your order has not been paid
        order_paid_yet = OrderCheckError.check_order_paid_yet(order_id)
        if order_paid_yet is not None:
            return order_paid_yet
            
        # Check if your order has been refund
        order_refund_yet = OrderCheckError.check_order_refund(order_id=order_id)
        if order_refund_yet is not None:
            return order_refund_yet

        refund = StripeAPI.refund(order_id)
        
        if refund == False :
            return Response(data={"message":"There is something wrong! Maybe you got a refund"}, status=status.HTTP_400_BAD_REQUEST)
        
        if refund["status"] == "succeeded" :
            order = Order.objects.get(id=order_id)
            Order.objects.filter(id = order_id).update(refund=True)
            mess = "Your refund request has been accepted! The amount to be refunded is " + str(refund["amount"])+" "+ str(refund["currency"])+" for order "+ str(order_id)

            send_mail(
                "Refund Notifications",
                mess,from_mail,
                recipient_list=[str(order.email)]
            )
            mess = "You have refund with order id "+str(order_id)
            # Message.send_notification_with_firebase("Refund",mess)
            FCM.send_message_to("Refund", mess)

        return Response(data=refund, status=status.HTTP_200_OK)
       
        