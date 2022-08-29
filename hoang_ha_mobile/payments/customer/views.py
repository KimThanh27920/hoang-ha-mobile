from msvcrt import SEM_NOOPENFILEERRORBOX
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated

from base.services.notifications.firebase_messaging import Message, FCM
from base.services.stripe.stripe_api import StripeAPI
from hoang_ha_mobile.base.errors import OrderCheckError

from accounts.models import StripeAccount
from accounts.customer.serializers import StripeAccountSerializer
from orders.models import Order



# Checkout with Payment Intent
class PaymentIntentCreateAPI(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]

    def post(self,request):
        order_id = request.data["order_id"]
        payment_method_types = [request.data["payment_method_types"]]

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
        if self.request.user.id is not None:
            if StripeAccount.objects.filter(user=self.request.user.id).exists() :
                stripe_obj = StripeAccount.objects.get(user=self.request.user.id)
                stripe_account_serializer = StripeAccountSerializer(stripe_obj)
                stripe_account = stripe_account_serializer.data["stripe_account"]
                intent = StripeAPI.create_payment_intent(order.total,"vnd",payment_method_types, order_id,stripe_account,self.request.user.id)
            else:
                intent = StripeAPI.create_payment_intent(order.total,"vnd",payment_method_types, order_id,self.request.user.id)
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
            if confirm["status"] == "succeeded":
                Order.objects.filter(id = payment_intent.metadata['order_id']).update(paid=True)
                mess = "You have a transation with order id "+ str(payment_intent.metadata['order_id'])
                
                # Message.send_notification_with_firebase("Checkout successful",mess)
               
                FCM.send_message_to("Checkout", mess)
            
            return Response(data=confirm , status=status.HTTP_200_OK)
       
        else:
            status_payment = payment_intent.status
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)



# Setup Intent 
class SetupIntent(APIView):
    
    #authentication_classes = [authentication.JWTAuthentication]

    def post(self, request):
        
        payment_method_types  = request.data['payment_method_types']

        if self.request.user.id is not None:
            setup_intent= StripeAPI.setup_intent(payment_method_types,user_id = self.request.user.id)
            client_secret = {
                "client_secret":setup_intent["client_secret"],
                "customer": self.request.user.id
                }
            return Response(data=setup_intent , status=status.HTTP_200_OK)
        
        setup_intent = StripeAPI.setup_intent(payment_method_types)
        client_secret = {"client_secret":setup_intent["client_secret"]}

        return Response(data=client_secret , status=status.HTTP_200_OK)



# Setup Intent 
class SetupIntentConfirmAPI(APIView):
    
    # authentication_classes = [authentication.JWTAuthentication]
    
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


# Refund 
class RefundAPI(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]


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

        order_check_status = OrderCheckError.check_valid_order_refund(order_id)

        if order_check_status is not None:
            mess =  "You have a request refund with order id "+str(order_id) 
            FCM.send_message_to("Refund",mess)
            return order_check_status

        refund = StripeAPI.refund(order_id)
        if refund == False :
            return Response(data={"message":"There is something wrong! Maybe you got a refund"}, status=status.HTTP_400_BAD_REQUEST)
        
        if refund["status"] == "succeeded" :
            
            Order.objects.filter(id = order_id).update(refund=True)
            mess = "You have refund with order id "+str(order_id)
            # Message.send_notification_with_firebase("Refund",mess)
            FCM.send_message_to("Checkout", mess)

        return Response(data=refund, status=status.HTTP_200_OK)