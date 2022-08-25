from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt import authentication

from base.services.notifications.firebase_messaging import send_notification_with_firebase
from hoang_ha_mobile.base.errors import check_valid_item

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
            
            send_notification_with_firebase("Create Order","You have a new order!")
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)


