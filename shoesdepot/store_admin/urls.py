from django.urls import path, include
from .views import ProductCreateView, ProductDeleteView, ProductUpdateView, ProductListView

urlpatterns = [
    path('', ProductListView.as_view(), name='admin_products_list'),
    path('create', ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', ProductUpdateView.as_view(), name='product_edit'),
    path('delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
]
