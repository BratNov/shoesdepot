from django.db import models
from django.utils.text import slugify
from .validators import validate_product_price


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.name}')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent.name} {self.name}" if self.parent else self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2, validators=[validate_product_price])
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products')
    is_on_sale = models.BooleanField(default=False)
    sale_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True,
                                     validators=[validate_product_price])
    sizes = models.ManyToManyField(Size, through='ProductSize')
    slug = models.SlugField(unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.name}')
        super().save(*args, **kwargs)

    def get_discount_percent(self):
        if not self.sale_price or not self.price:
            return 0

        discount = (self.price - self.sale_price) / self.price
        return round(discount * 100, 0)

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
