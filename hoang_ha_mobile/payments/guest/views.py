from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from base.services.notifications.firebase_messaging import Message, FCM
from base.services.stripe.stripe_api import StripeAPI
from hoang_ha_mobile.base.errors import OrderCheckError

from orders.models import Order


# Setup Intent 
class SetupIntent(APIView):
    
    #authentication_classes = [authentication.JWTAuthentication]

    def post(self, request):
        order_id  = request.data['order_id']
        payment_method_types  = request.data['payment_method_types']

        # Check order exists
        order_exist = OrderCheckError.check_order_exists(order_id)
        if order_exist is not None:
            return order_exist    
        
        # Check if your order has been paid
        order_paid_yet = OrderCheckError.check_order_paid(order_id)
        if order_paid_yet is not None:
            return order_paid_yet

        if self.request.user.id is not None:
            setup_intent= StripeAPI.setup_intent(payment_method_types,order_id,user_id = self.request.user.id)
            return Response(data=setup_intent , status=status.HTTP_200_OK)
        
        setup_intent = StripeAPI.setup_intent(payment_method_types,order_id)
        return Response(data=setup_intent , status=status.HTTP_200_OK)



# Setup Intent 
class SetupIntentConfirmAPI(APIView):
    
    #authentication_classes = [authentication.JWTAuthentication]

    def post(self, request):
        seti=request.data["setup_intent_id"]
        payment_method = request.data["payment_method"]
        setup_intent = StripeAPI.retrieve_setup_intent(seti)
        
        if setup_intent.status == "requires_payment_method" or setup_intent.status == "requires_confirmation":
            seti_confirm = StripeAPI.confirm_setup_intent(seti,payment_method=payment_method) 
            
            if seti_confirm.status == "succeeded":
                Order.objects.filter(id = seti_confirm.metadata['order_id']).update(paid=True)
                mess = "You have a transation with order id "+str(seti_confirm.metadata['order_id'])
                # Message.send_notification_with_firebase("Refund",mess)
                FCM.send_message_to("Checkout", mess)

            return Response(data=seti_confirm , status=status.HTTP_200_OK)
        else:
            status_payment = seti_confirm.status
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



