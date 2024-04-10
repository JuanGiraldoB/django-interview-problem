from django.db import models
from django.core.validators import MinValueValidator


# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='restaurant_logos/')

    def __str__(self) -> str:
        return f"{self.id} - {self.name}"


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.id} - {self.name} - {self.price}"


class Order(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100, null=True)
    is_takeaway = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=[
        ('ESPERA', 'En espera'),
        ('PREPARACION', 'En preparación'),
        ('COMPLETADO', 'Completado'),
    ], default='ESPERA')
    date = models.DateTimeField(null=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.id} - {self.restaurant.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)], default=1)
    special_instructions = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.order.restaurant} - {self.order.id}"
