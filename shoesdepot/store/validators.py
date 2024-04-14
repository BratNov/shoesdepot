from django.core.exceptions import ValidationError


def validate_product_price(value):
    if value < 0:
        raise ValidationError('Price cannot be negative.')
