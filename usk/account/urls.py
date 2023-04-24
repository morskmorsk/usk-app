from django.urls import path
from . import views

app = 'account'

urlpatterns = [
    # ... other URL patterns ...
    path('signup/', views.SignupView.as_view(), name='signup'),
]
