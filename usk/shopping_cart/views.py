from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (
    ListView, DetailView, CreateView, TemplateView, DeleteView)
from .models import (
    Product, ShoppingCart, ShoppingCartItem, Order, OrderItem)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm
from django.shortcuts import render
from django.http import Http404
from .forms import UpdateCartItemForm
from django.views.generic.edit import UpdateView
from django.views import View


class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'shopping_cart/product_list.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'shopping_cart/product_detail.html'


class AddProductView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopping_cart:product_list')


class UpdateProductView(LoginRequiredMixin, UpdateView):
    model = Product
    fields = ['name', 'price']
    success_url = reverse_lazy('shopping_cart:product_list')


class ShoppingCartView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping_cart/shopping_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(ShoppingCart, user=self.request.user)
        items = ShoppingCartItem.objects.filter(cart=cart)

        # Calculate the subtotal
        subtotal = sum([item.price * item.quantity for item in items])

        # Calculate the sales tax
        sales_tax = cart.get_sales_tax()

        # Calculate the total
        total = subtotal + sales_tax

        context.update({'items': items, 'subtotal': subtotal,
                        'sales_tax': sales_tax, 'total': total})
        return context


class AddToCartView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        price = request.POST.get('price', 0)
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart, _ = ShoppingCart.objects.get_or_create(user=request.user)
        item, created = ShoppingCartItem.objects.get_or_create(
            cart=cart, product=product, price=price)

        if not created:
            item.quantity += 1
            item.save()

        return redirect('shopping_cart:shopping_cart')


class RemoveFromCartView(LoginRequiredMixin, DeleteView):
    model = ShoppingCartItem
    success_url = reverse_lazy('shopping_cart:shopping_cart')

    def get_object(self, queryset=None):
        cart = get_object_or_404(ShoppingCart, user=self.request.user)
        cart_item = ShoppingCartItem.objects.filter(
            cart=cart, pk=self.kwargs['pk']).first()

        if not cart_item:
            raise Http404("Shopping cart item not found")

        return cart_item

    def render_to_response(self, context, **response_kwargs):
        if not context.get('object'):
            return render(self.request, 'shopping_cart/product_not_found.html',
                          status=404)

        return super().render_to_response(context, **response_kwargs)


class UpdateCartItemView(LoginRequiredMixin, UpdateView):
    model = ShoppingCartItem
    form_class = UpdateCartItemForm
    template_name = 'shopping_cart/update_cart_item.html'
    success_url = reverse_lazy('shopping_cart:shopping_cart')

    def get_queryset(self):
        return ShoppingCartItem.objects.filter(cart__user=self.request.user)


class CheckoutView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping_cart/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any context data needed for the checkout process here
        return context

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(ShoppingCart, user=request.user)
        cart_items = ShoppingCartItem.objects.filter(cart=cart)

        # Create Order
        order = Order(user=request.user)
        order.save()

        # Create OrderItems
        for item in cart_items:
            order_item = OrderItem(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.price
            )
            order_item.save()

        # Clear the cart
        cart_items.delete()

        # Redirect to a success page or any other appropriate page
        return redirect('shopping_cart:checkout_success')


class CheckoutSuccessView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping_cart/checkout_success.html'

# logout the user when the checkout is successful
    def get(self, request, *args, **kwargs):
        from django.contrib.auth import logout
        logout(request)
        return super().get(request, *args, **kwargs)