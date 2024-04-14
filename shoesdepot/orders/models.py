from django.contrib.auth import get_user_model
from django.db import models
from ..store.models import Product
from ..store.models import Size

UserModel = get_user_model()


class Order(models.Model):
    PENDING = 'PENDING'
    PROCESSING = 'PROCESSING'
    SHIPPED = 'SHIPPED'
    COMPLETED = 'COMPLETED'
    CANCELED = 'CANCELED'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSING, 'Processing'),
        (SHIPPED, 'Shipped'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Order №{self.pk} {self.date_ordered} from {self.user} status {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} - {self.size} x {self.quantity} ({self.order})"


class OrderAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postcode = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return (f"{self.first_name} {self.last_name}, {self.phone_number} {self.address}, {self.postcode} {self.city}, "
                f"{self.country}")
