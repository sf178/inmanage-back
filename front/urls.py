from django.urls import path, include
from .views import (
    LoginView, RegisterView, ConfirmRegistrationView, RefreshView, UserProfileView, MeView, LogoutView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("profile", UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('register/confirm', ConfirmRegistrationView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('me', MeView.as_view()),
    # path('profile/', UserProfileRetrieveUpdateView.as_view(), name='user-profile'),
    # path('profile/update/', UserProfilePartialUpdateView.as_view(), name='user-profile-partial-update'),
    path('logout', LogoutView.as_view()),
]