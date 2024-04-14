from django.urls import path
from .views import OrdersListView, OrderDetailView

urlpatterns = [
    path('', OrdersListView.as_view(), name='orders_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
]

