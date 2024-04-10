from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum, F
import json


from django.views.generic import View
from .models import (
    Order,
    Product,
    Restaurant,
    OrderItem
)

from .forms import (
    OrderItemForm
)


class IndexView(View):
    def get(self, request):
        return redirect('item_orders', restaurant_id=1)


class OrderItemsView(View):
    def get(self, request, restaurant_id: int):
        form = OrderItemForm()

        restaurant = Restaurant.objects.get(pk=restaurant_id)
        order = Order.objects.create(restaurant=restaurant)
        products = Product.objects.filter(restaurant_id=restaurant_id)

        context = {
            'restaurant': restaurant,
            'order_id': order.id,
            'products': products,
            'form': form,
            'customer_name': None
        }
        return render(request, 'orders/item_orders.html', context)

    def post(self, request, restaurant_id: int):
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_id = request.POST.get('order_id')
            order = Order.objects.get(pk=order_id)
            form.instance.order = order
            form.save()

            # Avoid n + 1 problem
            order_item = OrderItem.objects.select_related(
                'product').get(pk=form.instance.pk)

            context = {
                'success': True,
                'order_item': {
                    'name': order_item.product.name,
                    'quantity': order_item.quantity,
                    'details': order_item.special_instructions
                }
            }
            return JsonResponse(context)
        return JsonResponse({'errors': form.errors}, status=400)


class OrdersView(View):
    def get(self, request, restaurant_id: int, customer_name: str):
        orders = Order.objects.filter(restaurant_id=restaurant_id)
        context = {
            'orders': orders,
            'customer_name': customer_name
        }

        for order in orders:
            # Get the order items associated with the order and annotate the quantity for each product
            order_items = OrderItem.objects.filter(order=order).select_related(
                'product').annotate(total_quantity=Sum('quantity'))
            # Create a dictionary to store product quantities
            product_quantities = {}
            # Populate the product quantities dictionary
            for item in order_items:
                product_quantities[item.product] = item.total_quantity
            # Add the product quantities dictionary to the order context
            order.product_quantities = product_quantities

        print(order.customer_name)

        return render(request, 'orders/orders.html', context)

    def post(self, request, restaurant_id: int, customer_name: str):
        order_id = request.POST.get('order_id')
        customer_name = request.POST.get('customer_name')
        is_takeawy = request.POST.get('is_takeaway')

        order = Order.objects.get(pk=order_id)
        order.customer_name = customer_name
        order.date = timezone.now()
        order.is_takeaway = True if is_takeawy else False

        order_total = OrderItem.objects.filter(order=order).annotate(
            total_item_value=Sum(F('quantity') * F('product__price'))
        ).aggregate(total=Sum('total_item_value'))

        order.total = order_total['total']
        order.save()
        return redirect('orders', restaurant_id=restaurant_id, customer_name=customer_name)

    def put(self, request, restaurant_id: int, customer_name: str):
        data = json.loads(request.body)
        order_ids = data.get('order_ids', [])
        order_status = data.get('status', '')

        for order_id in order_ids:
            order = Order.objects.get(id=order_id)
            order.status = 'PREPARACION' if order_status == 'preparar' else 'COMPLETADO'
            print(order.status)
            order.save()

        return JsonResponse({'success': True})


class InvoiceView(View):
    def get(self, request, restaurant_id: int, customer_name: str, order_id: int):

        restaurant = get_object_or_404(
            Restaurant,
            id=restaurant_id
        )

        order = get_object_or_404(
            Order,
            id=order_id,
            restaurant_id=restaurant_id,
            customer_name=customer_name
        )
        order_items = OrderItem.objects.filter(
            order=order).select_related('product')

        product_quantities = {}
        for order_item in order_items:
            product_quantities[order_item.product] = order_item.quantity

        context = {
            'order': order,
            'product_quantities': product_quantities,
            'restaurant': restaurant
        }

        return render(request, 'orders/invoice.html', context)
