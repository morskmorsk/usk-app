from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import render, redirect


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            # Change 'home' to the name of the view you want to
            # redirect to after successful registration
            return redirect('shopping_cart:product_list')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
