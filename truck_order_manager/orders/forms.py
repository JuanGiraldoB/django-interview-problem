from django import forms
from .models import Restaurant, Product, Order, OrderItem


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'logo']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'is_takeaway']
        labels = {
            'customer_name': 'Nombre del pedido',
            'is_takeaway': 'Es para llevar?'
        }


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['product', 'quantity', 'special_instructions']
        labels = {
            'special_instructions': 'Observaciones adicionales',
            'product': 'Producto',
            'quantity': 'Cantidad'
        }
