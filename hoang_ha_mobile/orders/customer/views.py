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
        
    
    def get_serializer(self, *args, **kwargs):
        if(self.request.method == "GET"):
            return super().get_serializer(*args, **kwargs)
        return serializers.OrderSerializer(*args, **kwargs)
   
    
    def post(self, request, *args, **kwargs):
        serializer = serializers.OrderSerializer(data=request.data.get('order'))
            
        if(serializer.is_valid()):
            self.instance = serializer.save(created_by=self.request.user)
            instance_price = 0
            # print(self.instance.id)
            dt = self.request.data.get("order_detail")
            for d in dt:
                variant = Variant.objects.get(id=d.get('variant'))
                instance_price += int(variant.price) * int(d.get('quantity'))
                data = {
                    "order": self.instance.id,
                    "variant": d.get('variant'),
                    "quantity": d.get('quantity'),
                    "price": variant.price
                }
                serializer = serializers.OrderDetailSerializer(data=data)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = instance_price
            self.instance.save()
            print(self.instance)
            serializer = self.get_serializer(self.instance)
            return response.Response(data=serializer.data)
        else:
            return response.Response(serializer.errors)


# class ListOrderOwner(generics.ListAPIView):
#     serializer_class = serializers.OrderSerializer
#     def get_queryset(self):
#         self.queryset = models.Order.objects.filter(created_by = self.request.user.id)
#         return super().get_queryset()