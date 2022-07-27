from urllib import response
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .serializers import OrderSerializer, OrderDetailSerializer, CancelOrderSerializer, ListOrderSerializer
from ..models import Order, OrderDetail
from variants.models import Variant


class CreateOrderApiView(generics.ListCreateAPIView):

    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = Order.objects.filter(
            email=self.request.query_params.get('email')).prefetch_related()
        return super().get_queryset()

    def get_serializer(self, *args, **kwargs):
        if(self.request.method == "POST"):
            return super().get_serializer(*args, **kwargs)
        return ListOrderSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data.get('order'))

        if(serializer.is_valid()):
            self.instance = serializer.save()
            total = 0
            # print(self.instance.id)
            order_detail = self.request.data.get("order_details")
            for data in order_detail:
                variant = Variant.objects.get(id=data.get('variant'))
                if variant.sale:
                    price = variant.sale
                    total += int(variant.sale) * int(data.get('quantity'))
                else:
                    price = variant.price
                    total += int(variant.price) * int(data.get('quantity'))
                data_save = {
                    "order": self.instance.id,
                    "variant": data.get('variant'),
                    "quantity": data.get('quantity'),
                    "price": price
                }
                serializer = OrderDetailSerializer(data=data_save)
                if(serializer.is_valid()):
                    serializer.save()
            self.instance.total = total
            self.instance.save()
            print(self.instance)
            serializer = self.get_serializer(self.instance)
            return Response(data=serializer.data)
        else:
            return Response(serializer.errors)


class OrderDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = CancelOrderSerializer
    queryset = Order.objects.all().prefetch_related()
    lookup_url_kwarg = "order_id"

    # def update(self, request, *args, **kwargs):
    #     response = super().update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        try:
            data = Order.objects.get(id=self.kwargs['order_id'])
            if data.status == "Chờ xác nhận":
                return super().update(request, *args, **kwargs)
            else:
                return Response(data={"message": "Hông cho bé ơi!"})
        except:
            return Response(data={"detail": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)
