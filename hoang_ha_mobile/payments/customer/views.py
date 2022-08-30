from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated

from base.services.notifications.firebase_messaging import Message, FCM
from base.services.stripe.stripe_api import StripeAPI
from hoang_ha_mobile.base.errors import OrderCheckError
from hoang_ha_mobile.base.errors import check_valid_item

from accounts.models import StripeAccount
from orders.models import Order
from orders.customer.serializers import OrderSerializer, OrderDetailSerializer
from variants.models import Variant



#Order and checkout with Stripe for customer who have account
class OrderAndCheckout(APIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request):
        
        #add order 
        serializer = OrderSerializer(data=request.data.get('order'))   
        array_order_detail = self.request.data.get("order_details")
        payment_method = self.request.data.get("payment_method")

        temp = check_valid_item(array_order_detail)
        
        if(temp is not None):
            return temp
        
        if(serializer.is_valid()):            
            self.instance = serializer.save(created_by=self.request.user)
            instance_price = 0
            
            temp = check_valid_item(array_order_detail)
            if(temp is not None):
                return temp
            
            for order_detail in array_order_detail:       
                variant = Variant.objects.get(id=order_detail.get('variant'))
               
                if(variant.sale > 0):
                    price = variant.sale
               
                else:
                    price = variant.price
               
                instance_price += int(price) * int(order_detail.get('quantity'))
                data = {
                    "order": self.instance.id,
                    "variant": order_detail.get('variant'),
                    "quantity": order_detail.get('quantity'),
                    "price": price
                }
                serializer = OrderDetailSerializer(data=data)
               
                if(serializer.is_valid()):
                    serializer.save()
            
            self.instance.total = instance_price
            self.instance.save()
            serializer = OrderSerializer(self.instance)
        
        # checkout with stripe
        if self.request.user.id is not None:
           
            if StripeAccount.objects.filter(user=self.request.user.id).exists() :
                stripe_obj = StripeAccount.objects.get(user=self.request.user.id)
                stripe_account = stripe_obj.stripe_account
                payment_intent = StripeAPI.create_payment_intent(self.instance.total,"vnd",['card'], self.instance.id,stripe_account, self.request.user.id)
                
                #check payment method of user
                isvalid_payment_method = OrderCheckError.check_valid_payment_method(user_id = self.request.user.id, payment_method=payment_method)
                
                if isvalid_payment_method is not None :
                    return isvalid_payment_method
            else:
                payment_intent = StripeAPI.create_payment_intent(self.instance.total,"vnd",['card'], self.instance.id, self.request.user.id)
        
        else:
            # payment_intent = StripeAPI.create_payment_intent(self.instance.total,"vnd",['card'], self.instance.id)
            message ={
                "message": "This is a payment function for customers who have an account. Please login or use another payment function!",     
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        
        payment_intent_id = payment_intent["id"]
       
        #check status to checkout
        if payment_intent["status"] == "requires_payment_method" or payment_intent["status"] == "requires_confirmation":
            confirm= StripeAPI.confirm_payment_intent(payment_intent_id,payment_method)
            
            #check confirm error
            if confirm["status"] is False :
                message = confirm
                return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

            # update database
            if confirm["status"] == "succeeded":
                Order.objects.filter(id = payment_intent["metadata"]['order_id']).update(paid=True)
                #send message
                mess = "You have a transation with order id "+ str(payment_intent["metadata"]['order_id'])
                FCM.send_message_to("Checkout", mess)
           
            data ={
                "order": serializer.data,
                "checkout": confirm
            }
            return Response(data=data , status=status.HTTP_200_OK)
       
        else:
            status_payment = payment_intent["status"]
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)


# Setup Intent 
class SetupIntent(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        
        payment_method_types  = request.data['payment_method_types']

        if self.request.user.id is not None:
            setup_intent= StripeAPI.setup_intent([payment_method_types],user_id = self.request.user.id)
            
            client_secret = {
                "customer": self.request.user.id,
                "client_secret":setup_intent["client_secret"],
                }
            
            return Response(data=client_secret , status=status.HTTP_200_OK)
        
        data ={
            "message": "User id is must request, please login"
        }

        return Response(data=client_secret , status=status.HTTP_200_OK)


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