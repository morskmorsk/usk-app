from django.urls import path
from .views import profile, ProfileEditView, ChangePasswordView, signup

app = 'account'

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/change', ChangePasswordView.as_view(), name='change_password'),
]
