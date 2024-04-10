from django.contrib import admin
from .models import (
    Restaurant,
    Product,
    Order,
    OrderItem
)

admin.site.register(Restaurant)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
