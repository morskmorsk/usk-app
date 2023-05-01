from django.urls import path
from .views import profile, ProfileEditView, ChangePasswordView, signup
from rest_framework.routers import DefaultRouter
from .api_views import UserViewSet

router = DefaultRouter()

app = 'account'

urlpatterns = [
    path('signup/', signup,
         name='signup'),
    path('profile/', profile,
         name='profile'),
    path('profile/edit/', ProfileEditView.as_view(),
         name='profile_edit'),
    path('profile/change', ChangePasswordView.as_view(),
         name='change_password'),
    path('users/', UserViewSet.as_view({'get': 'list'}),
         name='api_profile'),
]
