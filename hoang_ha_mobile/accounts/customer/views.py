from django.contrib.auth import get_user_model
User = get_user_model()
from .. import serializers
from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt import tokens

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    # model = User
    permission_classes = [permissions.AllowAny, permissions.IsAuthenticated]

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