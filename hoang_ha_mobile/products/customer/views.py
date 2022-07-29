from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework_simplejwt import authentication

from django.contrib.auth import get_user_model
User = get_user_model()

from . import serializers
from ..models import Product


class UpdateFavorite(generics.UpdateAPIView):
    serializer_class = serializers.ProductFavorite
    lookup_url_kwarg = 'product_id'
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = Product.objects.all()
        return super().get_queryset()
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.favorite.add(self.request.user)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

        
    