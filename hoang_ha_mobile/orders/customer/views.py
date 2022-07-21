from ast import Try
from . import serializers
from rest_framework import generics, permissions, response, status
from .. import models
from variants.models import Variant
from rest_framework_simplejwt import authentication

class CreateOrderAPIView(generics.ListCreateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.OrderSerializer
    
    def get_queryset(self):        
        self.queryset = models.Order.objects.filter(created_by=self.request.user.id)
        return super().get_queryset()
        
      
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderSerializer(data=request.data.get('order'))
            
        if(serializer.is_valid()):
            self.instance = serializer.save(created_by=self.request.user)
            instance_price = 0
            # print(self.instance.id)
            array_order_detail = self.request.data.get("order_detail")
            for order_detail in array_order_detail:
                try:
                    variant = Variant.objects.get(id=order_detail.get('variant'))
                except:
                    return response.Response(data={"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)
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
            # print(self.instance)
            serializer = self.get_serializer(self.instance)
            return response.Response(data=serializer.data)
        else:
            return response.Response(serializer.errors)


# class ListOrderOwner(generics.ListAPIView):
#     serializer_class = serializers.OrderSerializer
#     def get_queryset(self):
#         self.queryset = models.Order.objects.filter(created_by = self.request.user.id)
#         return super().get_queryset()