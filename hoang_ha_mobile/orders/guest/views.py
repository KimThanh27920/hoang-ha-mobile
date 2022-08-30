import json
import functools

from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView

from base.services.stripe.stripe_api import StripeAPI
from base.services.notifications.firebase_messaging import FCM

from variants.models import Variant
from hoang_ha_mobile.base.errors import check_valid_item
from .serializers import OrderSerializer, OrderDetailSerializer, ListOrderSerializer
from ..models import Order


class CreateOrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = Order.objects.filter(
            email=self.request.query_params.get('email').lower()).prefetch_related()
        return super().get_queryset()

    def get_serializer(self, *args, **kwargs):
        if(self.request.method == "POST"):
            return super().get_serializer(*args, **kwargs)
        return ListOrderSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['order']['email'] = request.data['order'].get(
            'email').lower()

        order_detail = self.request.data.get("order_details")
        items = check_valid_item(order_detail)
        if(items is not None):
            return items

        serializer = OrderSerializer(data=request.data.get('order'))
        if(serializer.is_valid()):
            self.instance = serializer.save()
            total = 0
            for data in order_detail:
                variant = Variant.objects.get(id=data.get(
                    'variant'), status=True, deleted_by=None)
                if variant.sale:
                    price = variant.sale
                    total += int(variant.sale) * int(data.get('quantity'))
                else:
                    price = variant.price
                    total += int(variant.price) * int(data.get('quantity'))
                data_save = {
                    "order": self.instance.id,
                    "variant": data.get('variant'),
                    "quantity": data.get('quantity'),
                    "price": price
                }
                serializer = OrderDetailSerializer(data=data_save)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = total
            self.instance.save()
            serializer = self.get_serializer(self.instance)
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class OrderDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related()
    lookup_url_kwarg = "order_id"

    def update(self, request, *args, **kwargs):
        data = get_object_or_404(Order, id=self.kwargs['order_id'])
        if data.status == "processing":
            serializer = self.get_serializer(
                data, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(data=serializer.data)
        else:
            return Response(data={"message": "Not Update!"}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

class CreatePaymentMethod(APIView):
    def post(self, request):
        request.data['card_number'] = request.data.get('card_number')
        request.data['exp_month'] = request.data.get('exp_month')
        request.data['exp_year'] = request.data.get('exp_year')
        request.data['cvc'] = request.data.get('cvc')
        #Create a Payment method
        stripe_payment = StripeAPI.create_payment_method(
            request.data['card_number'],
            request.data['exp_month'],
            request.data['exp_year'],
            request.data['cvc']
        )
        data = {
            "payment_method_id":stripe_payment["id"] 
        }
        return Response(data=data,status=status.HTTP_200_OK )

# API for order and checkout for customer who don't have account
class OrderAndCheckout(APIView):

    def post(self,request):
        
        #add order 
        serializer = OrderSerializer(data=request.data.get('order'))   
        array_order_detail = self.request.data.get("order_details")
        payment_method = self.request.data.get("payment_method")
        
        temp = check_valid_item(array_order_detail)
        
        if(temp is not None):
            return temp
        
        if(serializer.is_valid()):            
            self.instance = serializer.save()
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
        payment_intent = StripeAPI.create_payment_intent(self.instance.total,"vnd",['card'], self.instance.id)
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
            return Response(data=data, status=status.HTTP_200_OK)
       
        else:
            status_payment = payment_intent["status"]
            message ={
                "message": "Can't checkout",
                "status_payment" : status_payment
            }
            return Response(data=message, status=status.HTTP_400_BAD_REQUEST)

