from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import authentication

from hoang_ha_mobile.base.errors import OrderCheckError
from base.services.stripe.views import StripeAPI

from orders.models import Order
from accounts.models import StripeAccount
from accounts.customer.serializers import StripeAccountSerializer


# Checkout with Payment Intent
class PaymentIntentCreateAPI(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]

    def post(self,request):
        order_id = request.data["order_id"]
        payment_method_types = request.data["payment_method_types"]

        # Check order exists
        order_exist = OrderCheckError.check_order_exists(order_id)
        if order_exist is not None:
            return order_exist    
        
        # Check if your order has been paid
        order_paid_yet = OrderCheckError.check_order_paid(order_id)
        if order_paid_yet is not None:
            return order_paid_yet
           
        # get customer id
        order = Order.objects.get(id=order_id)
        if self.request.user.id is not None and StripeAccount.objects.filter(user=self.request.user.id).exists() :
            stripe_obj = StripeAccount.objects.get(user=self.request.user.id)
            stripe_account_serializer = StripeAccountSerializer(stripe_obj)
            stripe_account = stripe_account_serializer.data["stripe_account"]
            intent = StripeAPI.create_payment_intent(order.total,"vnd",payment_method_types, order_id,stripe_account)
        else:
            intent = StripeAPI.create_payment_intent(order.total,"vnd",payment_method_types, order_id)
        
        return Response(data=intent, status=status.HTTP_200_OK)
    
       

# Confirm Payment Intent
class PaymentIntentConfirmAPI(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]

    def post(self,request):
        payment_intent_id = request.data["payment_intent_id"]
        payment_method = request.data["payment_method"]
        payment_intent = StripeAPI.retrieve_payment_intent(payment_intent_id)
        
        #check payment method of user 
        isvalid_payment_method = OrderCheckError.check_valid_payment_method(user_id = self.request.user.id, payment_method=payment_method)
        if isvalid_payment_method is not None :
            return isvalid_payment_method

        #check status to checkout
        if payment_intent.status == "requires_payment_method" or payment_intent.status == "requires_confirmation":
            confirm= StripeAPI.confirm_payment_intent(payment_intent_id,payment_method)
            
            # update database
            if confirm.status == "succeeded":
                Order.objects.filter(id = payment_intent.metadata['order_id']).update(paid=True)

            return Response(data=confirm , status=status.HTTP_200_OK)
       
        else:
            status_payment = payment_intent.status
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
