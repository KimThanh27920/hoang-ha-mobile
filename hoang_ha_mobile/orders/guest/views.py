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
            if(len(order_detail) < 1):
                return Response(data = {"message": "Invalid data"})
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
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)


class OrderDetailApiView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().prefetch_related()
    lookup_url_kwarg = "order_id"
    

    # def update(self, request, *args, **kwargs):
    #     response = super().update(request, *args, **kwargs)

    # def get_serializer(self, *args, **kwargs):
    #     if(self.request.method == "PUT"):
    #         return super().get_serializer(*args, **kwargs)
    #     return OrderSerializer(*args, **kwargs)


    def update(self, request, *args, **kwargs):
        try:
            data = Order.objects.get(id=self.kwargs['order_id'])
            print(data)
            if data.status == "Chờ xác nhận":
                serializer = self.get_serializer(data, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(data=serializer.data)
            else:
                return Response(data={"message": "Not Update!"})
        except:
            return Response(data={"detail": "Not Found Order!"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
