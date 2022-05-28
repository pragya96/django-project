from django.db import models


# Create your models here.

class Store(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Categories'


class ProductAvailability(models.IntegerChoices):
    AVAILABLE = 1, "Available"
    NOT_AVAILABLE = 2, "Not Available"


class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=10)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    description = models.CharField(max_length=100, null=True, blank=True)
    availability = models.IntegerField(choices=ProductAvailability.choices)

    def __str__(self):
        return self.name

    def is_available(self):
        return self.availability == ProductAvailability.AVAILABLE and self.quantity > 0
