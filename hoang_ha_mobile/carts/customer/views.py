from rest_framework import generics, permissions, response
from . import serializers
from .. import models
from rest_framework_simplejwt import authentication
from .permissions import IsOwner

class CartOwnerCreateOrUpdateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(user = self.request.user.id)
        return super().get_queryset() 
    
    def post(self, request, *args, **kwargs):
        id = models.Cart.objects.filter(user = self.request.user.id, variant = int(self.request.data.get('variant')))
        if(id.exists()):
            # print(id[0].variant.id)
           
            quantity = request.data.get('quantity') + id[0].quantity
            data = {
                "variant": request.data.get('variant'),
                "quantity": quantity
            }
            serializer = serializers.CartSerializer(id[0], data=data)
            
        else:
            serializer = serializers.CartSerializer(data=self.request.data)
            
        if(serializer.is_valid()):
            serializer.save(user=self.request.user)
            return response.Response(True)
        else:
            return response.Response(serializer.errors)
        
class CartOwnerUpdateOrDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.CartUpdateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    lookup_url_kwarg = 'cart_id'
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(user = self.request.user.id).select_related()
        return super().get_queryset()