from rest_framework import generics, permissions, response, status
from . import serializers
from .. import models
from rest_framework_simplejwt import authentication
from .permissions import IsOwner


# TODO: @all: check the Code Lay-out here. All spacing between classes, functions must be consistent. See guidelines: https://peps.python.org/pep-0008/.

class CartOwnerCreateOrUpdateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.CartReadSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    pagination_class = None    
    
    def get_queryset(self):
        self.queryset = models.Cart.objects.filter(
            user=self.request.user.id).select_related()
        return super().get_queryset()

    def post(self, request, *args, **kwargs):
        try:
            id  = models.Cart.objects.filter(user = self.request.user.id, variant = int(self.request.data.get('variant')))
        except:
            return response.Response(data={"Error": "Lost data"},  status = status.HTTP_400_BAD_REQUEST)
        if(id.exists()):
            if not (request.data.get('quantity') > 0): 
               return response.Response(data={"Error": "Invalid quantity"},  status = status.HTTP_400_BAD_REQUEST)
            quantity = request.data.get('quantity') + id[0].quantity
            data = {
                "variant": request.data.get('variant'),
                "quantity": quantity
            }
            serializer = serializers.CartWriteSerializer(id[0], data=data)

        else:
            serializer = serializers.CartWriteSerializer(
                data=self.request.data)

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
        if(len(items) < 1): 
            return response.Response(data={"Error: Invalid data"}, status = status.HTTP_400_BAD_REQUEST)
        for item in items:
            if not (item.get('quantity') > 0): 
                return response.Response(data={"Error: Invalid quantity"}, status = status.HTTP_400_BAD_REQUEST)
        data_return = []
        for item in items:
            id = models.Cart.objects.filter(user = self.request.user.id, variant = int(item.get('variant')))
            if(id.exists()):
                
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
        self.queryset = models.Cart.objects.filter(
            user=self.request.user.id).select_related()
        return super().get_queryset()
