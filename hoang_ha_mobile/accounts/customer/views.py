from rest_framework import generics, permissions, response, status, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenBlacklistView, TokenRefreshView
from rest_framework_simplejwt import tokens, authentication
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .. import models
from . import serializers
from base.services.stripe.views import StripeAPI



User = get_user_model()


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = serializers.ChangePasswordSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
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
    pagination_class = None
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = models.Address.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    def perform_create(self, serializer):        
        serializer.save(user=self.request.user)
        
        
class AddressRetrieveDestroyUpdateAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AddressSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None
    lookup_url_kwarg = 'address_id'
    
    def get_queryset(self):
        self.queryset = models.Address.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    
class ProfileUpdateRetrieveAPIView(generics.RetrieveUpdateAPIView):
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if(self.request.method == "GET"):
            self.serializer_class = serializers.ProfileSerializer
        else:
            self.serializer_class = serializers.UserSerializer            
        return super().get_serializer_class()
    
    def get_object(self, queryset=None):
        obj = get_object_or_404(User,id=self.request.user.id)
        return obj    
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)
        
        
class UploadImageAPIView(generics.UpdateAPIView):

    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserUploadImage

    def get_object(self, queryset=None):
        obj = get_object_or_404(User,id=self.request.user.id)
        return obj    
    
    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user.id)


#Create Customer in Stripe and add Payment method
class PaymentMethodCreateAPIView(generics.GenericAPIView,mixins.CreateModelMixin):
    
    serializer_class = serializers.StripeAccountSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        self.queryset = models.StripeAccount.objects.filter(user=self.request.user.id)
        return super().get_queryset()
    
    def post(self, request):
        user = self.request.user.id
        request.data['card_number'] = request.data.get('card_number')
        request.data['exp_month'] = request.data.get('exp_month')
        request.data['exp_year'] = request.data.get('exp_year')
        request.data['cvc'] = request.data.get('cvc')

        customer = models.CustomUser.objects.get(id=self.request.user.id)
        customer_serializer = serializers.UserSerializer(customer)

        if not models.StripeAccount.objects.filter(user=user).exists() :
            
            #Create a Customer
            print("error")
            stripe_account = StripeAPI.create_customer(customer_serializer.data['email'])
            data_stripe_account = {
                "stripe_account" : stripe_account.id
            }
            serializer = self.get_serializer(data=data_stripe_account)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=self.request.user)    

        else: 
            #Stripe Account is exists
            stripe_obj = models.StripeAccount.objects.get(user=self.request.user.id)
            stripe_account_serializer = serializers.StripeAccountSerializer(stripe_obj)
            stripe_account = stripe_account_serializer.data["stripe_account"]
        
        # Create a Payment method
        stripe_payment = StripeAPI.create_payment_method(
            request.data['card_number'],
            request.data['exp_month'],
            request.data['exp_year'],
            request.data['cvc']
        )
        
        # Attach Payment method to a Customer
        StripeAPI.attach(stripe_payment,stripe_account)
        # List payment method 
        data = StripeAPI.get_list_payment_method(stripe_account)
        return Response(data=data, status=status.HTTP_200_OK)


class PaymentMethodListAPIView(APIView):
    
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request):
        user = self.request.user.id
        if models.StripeAccount.objects.filter(user=user).exists() :

            stripe_obj = models.StripeAccount.objects.get(user=user)
            stripe_account_serializer = serializers.StripeAccountSerializer(stripe_obj)
            stripe_account = stripe_account_serializer.data["stripe_account"]
            data = StripeAPI.get_list_payment_method(stripe_account)

            return Response(data=data, status=status.HTTP_200_OK)

        return Response({},status=status.HTTP_204_NO_CONTENT)


        