from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.ListCategoryApiView.as_view()),
]