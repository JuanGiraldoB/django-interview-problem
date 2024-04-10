from django.urls import path
from .views import (
    IndexView,
    OrderItemsView,
    OrdersView,
    InvoiceView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('create-order-items/<int:restaurant_id>',
         OrderItemsView.as_view(), name='item_orders'),
    path('order/<int:restaurant_id>/<str:customer_name>',
         OrdersView.as_view(), name='orders'),
    path('order/<int:restaurant_id>/<str:customer_name>/<int:order_id>',
         InvoiceView.as_view(), name='invoice'),
]
