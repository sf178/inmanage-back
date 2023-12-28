from django.urls import path, include
from .views import (
    LoginView, RegisterView, ConfirmRegistrationView, RefreshView, UserProfileView, UserProfilePartialUpdateView, MeView, LogoutView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

# router.register("profile/", UserProfileView)
# router.register("profile/up", UserProfilePartialUpdateView)
urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('register/confirm/', ConfirmRegistrationView.as_view(), name='register-confirm'),
    path('refresh/', RefreshView.as_view(), name='refresh'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]