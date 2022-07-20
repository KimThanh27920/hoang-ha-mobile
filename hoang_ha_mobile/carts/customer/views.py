from rest_framework import generics, permissions, response
from .. import serializers
from .. import models
from rest_framework_simplejwt import authentication

class CartOwnerAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
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