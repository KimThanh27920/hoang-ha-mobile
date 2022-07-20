from rest_framework.response import Response
from rest_framework import generics
from .serializers import OrderSerializer, OrderDetailSerializer
from ..models import Order, OrderDetail
from variants.models import Variant
class CreateOrderApiView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    def get_serializer(self, *args, **kwargs):
        return OrderSerializer(*args, **kwargs)
   
    
    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data.get('order'))
            
        if(serializer.is_valid()):
            self.instance = serializer.save()
            instance_price = 0
            # print(self.instance.id)
            dt = self.request.data.get("order_detail")
            for d in dt:
                variant = Variant.objects.get(id=d.get('variant'))
                instance_price += int(variant.price) * int(d.get('quantity'))
                data = {
                    "order": self.instance.id,
                    "variant": d.get('variant'),
                    "quantity": d.get('quantity'),
                    "price": variant.price
                }
                serializer = OrderDetailSerializer(data=data)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = instance_price
            print(self.instance)
            serializer = self.get_serializer(self.instance)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)

class OrderDetailApiView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related()
    lookup_url_kwarg = "order_id"

    # def retrieve(self, request, *args, **kwargs):
    #     data = super().retrieve(request, *args, **kwargs)
    #     # query = OrderDetail.objects.filter(order=self.kwargs['order_id'])
    #     # serializer = OrderDetailSerialize   r(query, many=True)
    #     return Response(data=data.data)