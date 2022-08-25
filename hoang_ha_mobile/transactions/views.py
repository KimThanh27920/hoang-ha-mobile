from rest_framework import generics, filters
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAdminUser

from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend

from accounts.models import CustomUser
from orders.models import Order
from .models import Transaction
from .serializers import TransactionSerializerList

# Create your views here.
def create_transaction(data):
    trans = Transaction( 
        datetime = data['datetime'],
        type = data['type'],
        amount = data['amount'],
        currency = data['currency'],
        description = data['description'],
        payment_intent = data['payment_intent'],
        last4 = data['last4']
    )
    order_id = data['order']
    user_id = data['customer']

    order = Order.objects.get(id = order_id)
    trans.order= order

    if user_id is not None:
        customer = CustomUser.objects.get(id= user_id)
        trans.customer = customer
    
    trans.save()
    
    return HttpResponse(status=200)

# transactions list view
class TransactionListAPI(generics.ListAPIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminUser]

    serializer_class = TransactionSerializerList
    queryset = Transaction.objects.all().order_by('-id')
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['order__id','customer__full_name','customer__email']
    filterset_fields = ['type']