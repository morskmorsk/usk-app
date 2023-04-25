from django.forms import ModelForm
from django import forms
from .models import Product, ShoppingCartItem


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'department', 'price', 'description', 'image',
                  'location', 'cost']


class UpdateCartItemForm(ModelForm):
    class Meta:
        model = ShoppingCartItem
        fields = ['quantity', 'price']
        widgets = {
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control', 'min': '1'})
        }
