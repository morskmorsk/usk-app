from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth import login
from .forms import SignupForm
from django.shortcuts import render, redirect
# views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.contrib import messages
from .forms import ProfileForm


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('shopping_cart:product_list')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def profile(request):
    return render(request, 'account/profile.html', {'user': request.user})


class ProfileEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)
        return render(request, 'account/profile_edit.html', {'form': form})

    def post(self, request):
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/profile_edit.html', {'form': form})


class ChangePasswordView(LoginRequiredMixin, View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        return render(request, 'account/change_password.html', {'form': form})

    def post(self, request):
        form = PasswordChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, 'Your password has been updated.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
        return render(request, 'account/change_password.html', {'form': form})
