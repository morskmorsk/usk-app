from django.contrib.auth import login
from .forms import CustomUserCreationForm
from django.views.generic import CreateView


class SignupView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'account/signup.html'
    success_url = 'shopping_cart/product_list'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response
