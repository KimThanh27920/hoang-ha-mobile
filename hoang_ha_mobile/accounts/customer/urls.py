from django.urls import path, include
from . import views
urlpatterns = [
    path('logout/', views.TokenBlacklistView.as_view(), name='logout'),
    path('refresh-token/', views.TokenRefreshView.as_view(), name='refresh_token'),
    path('profile/change_password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/addresses/', views.AddressListCreateAPIView.as_view(), name='create_addrress_list'),
    path('profile/addresses/<int:address_id>', views.AddressListCreateAPIView.as_view(), name='update_retrieve_destroy_address'),
    
]