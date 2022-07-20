from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.CommentListOwner.as_view(), name="list_comment"),
    path('products/<int:product_id>/', views.CommentListProduct.as_view(), name="list_comment_product"),
    path('<int:comment_id>/', views.CommentDetail.as_view(), name="comment_detail"),
]