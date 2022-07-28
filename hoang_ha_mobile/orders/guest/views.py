
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from variants.models import Variant
from .serializers import OrderSerializer, OrderDetailSerializer, ListOrderSerializer
from ..models import Order


class CreateOrderApiView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        self.queryset = Order.objects.filter(
            email=self.request.query_params.get('email').lower()).prefetch_related()
        return super().get_queryset()

    def get_serializer(self, *args, **kwargs):
        if(self.request.method == "POST"):
            return super().get_serializer(*args, **kwargs)
        return ListOrderSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['order']['email'] = request.data['order'].get(
            'email').lower()
        serializer = OrderSerializer(data=request.data.get('order'))
        if(serializer.is_valid()):
            order_detail = self.request.data.get("order_details")
            if(len(order_detail) < 1):
                return Response(data={"message": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            for data in order_detail:
                if not (int(data.get('quantity')) > 0):
                    return Response(data={"message": "Invalid quantity"}, status=status.HTTP_400_BAD_REQUEST)
            self.instance = serializer.save()
            total = 0
            # print(self.instance.id)
            for data in order_detail:
                try:
                    variant = Variant.objects.get(id=data.get('variant'), status=True, deleted_by=None)
                except:
                    return Response(data={"detail": "Variant not found"}, status=status.HTTP_404_NOT_FOUND)

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
            if data.status == "processing":
                serializer = self.get_serializer(
                    data, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)
                return Response(data=serializer.data)
            else:
                return Response(data={"message": "Not Update!"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(data={"detail": "Not Found Order!"}, status=status.HTTP_404_NOT_FOUND)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
