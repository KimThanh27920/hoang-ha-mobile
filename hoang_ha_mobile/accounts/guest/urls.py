from django.urls import path, include
from . import views
urlpatterns = [
    path('login/', views.LoginApiView.as_view()),
    path('register/', views.RegisterApiView.as_view())
]