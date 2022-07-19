from django.contrib.auth import get_user_model
User = get_user_model()
from .. import serializers
from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt import tokens, authentication
from .. import models
from django.shortcuts import get_object_or_404

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    # model = User
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]
    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return response.Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            
            self.object.save()
            refresh = tokens.RefreshToken.for_user(self.object)
            
            res = {
                'message': 'Password updated successfully',
                'token': {
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }
            }

            return response.Response(data=res, status=status.HTTP_200_OK)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class AddressListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = serializers.AddressSerializer
    # queryset = models.Address.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def get_queryset(self):
        self.queryset = models.Address.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    def perform_create(self, serializer):        
        serializer.save(user=self.request.user)
        
class AddressRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AddressSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    lookup_url_kwarg = 'address_id'
    def get_queryset(self):
        self.queryset = get_object_or_404(models.Address,user=self.request.user.id)
        return super().get_queryset()
        
class ProfileAPIView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer
    # queryset = User.objects.all()
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    pagination_class = None
    def get_queryset(self):
        self.queryset = User.objects.filter(id=self.request.user.id).prefetch_related()
        return super().get_queryset()
    # def get_serializer(self, *args, **kwargs):
    #     kwargs['addresses'] = models.Address.objects.filter(user=self.request.user.id)
    #     return super().get_serializer(*args, **kwargs)