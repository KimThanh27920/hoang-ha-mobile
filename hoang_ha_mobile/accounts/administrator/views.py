from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class UserListView(generics.ListAPIView):
    # TODO: Admin should have options to search, filter, ordering. See guideline: https://www.django-rest-framework.org/api-guide/filtering/#djangofilterbackend.
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()
