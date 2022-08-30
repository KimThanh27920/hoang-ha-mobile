import json

from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt import authentication
from rest_framework.views import APIView

from base.services.notifications.firebase_messaging import Message, FCM
from hoang_ha_mobile.base.errors import check_valid_item
from base.services.stripe.stripe_api import StripeAPI
from hoang_ha_mobile.base.errors import OrderCheckError

from accounts.customer.serializers import StripeAccountSerializer
from accounts.models import StripeAccount
from variants.models import Variant
from . import serializers
from .. import models



class ListCreateOrderAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderReadSerializer
    
    def get_queryset(self):        
        self.queryset = models.Order.objects.filter(created_by=self.request.user.id)
        return super().get_queryset()    
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderSerializer(data=request.data.get('order'))   
        array_order_detail = self.request.data.get("order_details")
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
                serializer = serializers.OrderDetailSerializer(data=data)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = instance_price
            self.instance.save()
           
            serializer = serializers.OrderSerializer(self.instance)

            FCM.send_message_to("Order Notification", "Have a order")

            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


#Order and checkout with Stripe for customer who have account
class OrderAndCheckout(APIView):
    authentication_classes = [authentication.JWTAuthentication]

    def post(self,request):
        
        #add order 
        serializer = serializers.OrderSerializer(data=request.data.get('order'))   
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
                serializer = serializers.OrderDetailSerializer(data=data)
               
                if(serializer.is_valid()):
                    serializer.save()
            
            self.instance.total = instance_price
            self.instance.save()
            serializer = serializers.OrderSerializer(self.instance)
        
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
            return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)
        
        payment_intent_id = payment_intent["id"]
       
        #check status to checkout
        if payment_intent["status"] == "requires_payment_method" or payment_intent["status"] == "requires_confirmation":
            confirm= StripeAPI.confirm_payment_intent(payment_intent_id,payment_method)
            
            #check confirm error
            if confirm["status"] is False :
                message = confirm
                return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)

            # update database
            if confirm["status"] == "succeeded":
                models.Order.objects.filter(id = payment_intent["metadata"]['order_id']).update(paid=True)
                #send message
                mess = "You have a transation with order id "+ str(payment_intent["metadata"]['order_id'])
                FCM.send_message_to("Checkout", mess)
           
            data ={
                "order": serializer.data,
                "checkout": confirm
            }
            return response.Response(data=data , status=status.HTTP_200_OK)
       
        else:
            status_payment = payment_intent["status"]
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return response.Response(data=message, status=status.HTTP_400_BAD_REQUEST)

