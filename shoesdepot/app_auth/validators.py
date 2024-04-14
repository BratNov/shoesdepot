from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator

name_validators = [
    MinLengthValidator(2, message="Name must be at least 2 characters."),
    MaxLengthValidator(20, message="Name cannot be longer than 20 characters."),
    RegexValidator(r'^[A-Za-z\s]+$', message='Name should contain only letters and spaces.')
]


def validate_phone_number(value):
    if not all(char.isdigit() for char in value):
        raise ValidationError('Phone number should contain only digits.')
    if len(value) < 10:
        raise ValidationError('Phone number should be at least 10 characters long.')
