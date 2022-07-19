from rest_framework import generics, permissions
from accounts.administrator.serializers import UserSerializer
from accounts.models import CustomUser as User
from rest_framework_simplejwt.authentication import JWTAuthentication


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
