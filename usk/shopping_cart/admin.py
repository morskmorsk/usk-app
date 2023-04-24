from django.contrib import admin
from .models import Product, ShoppingCart
from .models import ShoppingCartItem, Department, Location

admin.site.register(Product)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(Department)
admin.site.register(Location)
