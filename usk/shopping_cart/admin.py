from django.contrib import admin
from .models import (
    Product, ShoppingCart, ShoppingCartItem,
    Order, OrderItem, Department, Location)

admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Department)
admin.site.register(Location)
admin.site.register(Order)
admin.site.register(OrderItem)
