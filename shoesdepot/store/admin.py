from django.contrib import admin
from .models import Category, Product, Size, ProductSize

admin.site.register(Category)
admin.site.register(Size)


class ProductSizeInline(admin.TabularInline):
    model = ProductSize


class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductSizeInline]


admin.site.register(Product, ProductAdmin)
