from django.urls import path
from .views import cart_add_view, cart_summary_view, cart_delete_view, cart_update_view, CartCheckoutView

urlpatterns = [
    path('', cart_summary_view, name='cart_summary'),
    path('add', cart_add_view, name="cart_add"),
    path('delete/<str:cart_key>/', cart_delete_view, name="cart_delete"),
    path('update/<str:cart_key>/', cart_update_view, name="cart_update"),
    path('checkout', CartCheckoutView.as_view(), name="cart_checkout"),
]
