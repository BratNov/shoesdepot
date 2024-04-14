from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<str:slug>/', views.product_details, name='product_details'),
    path('category/<str:category_slug>/<str:subcategory_slug>/', views.category_details, name='category_details'),
]
