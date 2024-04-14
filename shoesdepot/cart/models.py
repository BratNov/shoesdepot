from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Cart(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name='cart')
    cart_data = models.JSONField(default=dict)
    cart_items = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart for {self.user}"
