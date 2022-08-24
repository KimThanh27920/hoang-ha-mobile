from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt import authentication

from hoang_ha_mobile.base.errors import OrderCheckError
from base.services.stripe.views import StripeAPI






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
        
        # Check if your order has been refund
        order_refund_yet = OrderCheckError.check_order_refund(order_id=order_id)
        if order_refund_yet is not None:
            return order_refund_yet
        
        # Check if your order has not been paid
        order_paid_yet = OrderCheckError.check_order_paid_yet(order_id)
        if order_paid_yet is not None:
            return order_paid_yet

        refund = StripeAPI.refund(order_id)
        return Response(data=refund, status=status.HTTP_200_OK)
       
        