from django.urls import path
from .views import (
    ProductListView,
    ProductDetailView,
    AddProductView,
    UpdateProductView,
    ShoppingCartView,
    AddToCartView,
    RemoveFromCartView,
    UpdateCartItemView,
    CheckoutView,
    CheckoutSuccessView,
)

app_name = 'shopping_cart'

urlpatterns = [
     path('', ProductListView.as_view(), name='product_list'),
     path('product_detail/<int:pk>/', ProductDetailView.as_view(),
          name='product_detail'),
     path('add_product/', AddProductView.as_view(),
          name='add_product'),
     path('update_product/<int:pk>/', UpdateProductView.as_view(),
          name='update_product'),
     path('shopping_cart/', ShoppingCartView.as_view(),
          name='shopping_cart'),
     path('add_to_cart/<int:pk>/', AddToCartView.as_view(),
          name='add_to_cart'),
     path('remove_from_cart/<int:pk>/', RemoveFromCartView.as_view(),
          name='remove_from_cart'),
     path('update_cart_item/<int:pk>/', UpdateCartItemView.as_view(),
          name='update_cart_item'),
     path('checkout/', CheckoutView.as_view(), name='checkout'),
     path('checkout_success/', CheckoutSuccessView.as_view(),
          name='checkout_success'),
]
