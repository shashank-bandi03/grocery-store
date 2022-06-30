from django.urls import path

from . import views

urlpatterns = [
    path('register', views.UserRegistrationView.as_view(), name='User Registration API'),
    path('login', views.UserLoginView.as_view(), name='User Login API'),
    path('logout', views.UserLogoutView.as_view(), name='User Logout API'),
    path('items/<int:pk>/', views.ItemDetail.as_view(), name='Item Detail API'),
    path('items/', views.ItemListView.as_view(), name='List Items API'),
    path('order/', views.OrderListView.as_view(), name='List Orders API'),
    path('orders_list/', views.UserOrderListView.as_view(), name='List User Orders API')
]