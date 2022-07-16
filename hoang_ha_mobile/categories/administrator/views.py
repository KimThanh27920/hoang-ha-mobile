from rest_framework import viewsets,status
from rest_framework.response import Response
from categories.serializers import CategorySerializer
from categories.models import Category

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_204_NO_CONTENT)
        # return super().destroy(request, *args, **kwargs)