from django.contrib import admin
from .models import Order, OrderAddress, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem


class OrderAddressInline(admin.TabularInline):
    model = OrderAddress


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, OrderAddressInline]


admin.site.register(Order, OrderAdmin)
