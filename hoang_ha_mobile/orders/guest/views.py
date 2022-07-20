from rest_framework.response import Response
from rest_framework import generics
from .serializers import OrderSerializer, OrderDetailSerializer
from ..models import Order, OrderDetail
class OrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

class OrderDetailApiView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    lookup_url_kwarg = "order_id"

    # def retrieve(self, request, *args, **kwargs):
    #     data = super().retrieve(request, *args, **kwargs)
    #     # query = OrderDetail.objects.filter(order=self.kwargs['order_id'])
    #     # serializer = OrderDetailSerializer(query, many=True)
    #     return Response(data=data.data)