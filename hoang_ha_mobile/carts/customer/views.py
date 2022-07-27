from rest_framework import generics, permissions, response, status
from . import serializers
from .. import models
from rest_framework_simplejwt import authentication
from .permissions import IsOwner

class CartOwnerCreateOrUpdateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CartReadSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = None    
    
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(user = self.request.user.id).select_related()
        return super().get_queryset() 
    
    def post(self, request, *args, **kwargs):
        id = models.Cart.objects.filter(user = self.request.user.id, variant = int(self.request.data.get('variant')))
        if(id.exists()):
            if not (request.data.get('quantity') > 0): 
               return response.Response(data={"Error: Invalid quantity"})
            quantity = request.data.get('quantity') + id[0].quantity
            data = {
                "variant": request.data.get('variant'),
                "quantity": quantity
            }
            serializer = serializers.CartWriteSerializer(id[0], data=data)
            
        else:
            serializer = serializers.CartWriteSerializer(data=self.request.data)
            
        if(serializer.is_valid()):
            self.instance = serializer.save(user=self.request.user)
            serializer = serializers.CartReadSerializer(self.instance)
            return response.Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return response.Response(serializer.errors)

class CartListAddAPIView(generics.CreateAPIView):
    serializer_class = serializers.CartWriteSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(user = self.request.user.id).select_related()
        return super().get_queryset() 
    
    def post(self, request, *args, **kwargs):
        items = self.request.data.get('items')
        data_return = []
        for item in items:
            id = models.Cart.objects.filter(user = self.request.user.id, variant = int(item.get('variant')))
            if(id.exists()):
                if not (item.get('quantity') > 0): 
                    return response.Response(data={"Error: Invalid quantity"})
                quantity = item.get('quantity') + id[0].quantity
                data = {
                    "variant": item.get('variant'),
                    "quantity": quantity
                }
                serializer = serializers.CartWriteSerializer(id[0], data=data)
                
            else:
                serializer = serializers.CartWriteSerializer(data=item)
                
            if(serializer.is_valid()):
                self.instance = serializer.save(user=self.request.user)
                serializer = serializers.CartReadSerializer(self.instance)
                data_return.append(serializer.data)
            else:
                return response.Response(serializer.errors)
        return response.Response(data=data_return, status=status.HTTP_201_CREATED)
class CartOwnerUpdateOrDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CartUpdateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    lookup_url_kwarg = 'cart_id'
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(user = self.request.user.id).select_related()
        return super().get_queryset()