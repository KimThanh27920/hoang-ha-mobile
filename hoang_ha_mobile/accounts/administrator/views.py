from rest_framework import generics
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model
class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User().objects.all()
