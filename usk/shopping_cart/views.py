from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, TemplateView, DeleteView
from .models import Product, ShoppingCart, ShoppingCartItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .forms import ProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'shopping_cart/product_list.html'
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shopping_cart/product_detail.html'


class AddProductView(CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('shopping_cart:product_list')


class UpdateProductView(UpdateView):
    model = Product
    fields = ['name', 'price']
    success_url = reverse_lazy('shopping_cart:product_list')


class ShoppingCartView(LoginRequiredMixin, TemplateView):
    template_name = 'shopping_cart/shopping_cart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = get_object_or_404(ShoppingCart, user=self.request.user)
        items = ShoppingCartItem.objects.filter(cart=cart)
        sales_tax = cart.get_sales_tax()
        total_price = sum([item.price * item.quantity for item in items]) + sales_tax
        context.update({'items': items, 'sales_tax': sales_tax, 'total_price': total_price})
        return context


class AddToCartView(LoginRequiredMixin, TemplateView):

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
    success_url = reverse_lazy('shopping_cart')

    def get_object(self, queryset=None):
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart = get_object_or_404(ShoppingCart, user=self.request.user)
        return get_object_or_404(ShoppingCartItem, cart=cart, product=product)


class UpdateCartItemView(LoginRequiredMixin, TemplateView):

    def post(self, request, *args, **kwargs):
        quantity = int(request.POST.get('quantity', 1))
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        cart = get_object_or_404(ShoppingCart, user=request.user)
        item = get_object_or_404(ShoppingCartItem, cart=cart, product=product)

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

        return redirect('shopping_cart')
