from django.urls import path, include
from . import views
urlpatterns = [
    path('logout/', views.TokenBlacklistView.as_view(), name='logout'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='refresh_token'),
]