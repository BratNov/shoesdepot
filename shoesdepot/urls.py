from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import PasswordResetView

urlpatterns = [
    path('', include('shoesdepot.store.urls')),
    path('admin/', admin.site.urls),
    path('user/', include('shoesdepot.app_auth.urls')),
    path('cart/', include('shoesdepot.cart.urls')),
    path('store_admin/', include('shoesdepot.store_admin.urls')),
    path('orders/', include('shoesdepot.orders.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

