from django.urls import path
from .views import (
    DashboardView, ProfileUpdateView, UserPasswordChangeView,
    UserRegisterView, UserLoginView, logout_view
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("register/", UserRegisterView.as_view(), name="register"),
    path("logout/", logout_view, name="logout"),
    path("settings/", ProfileUpdateView.as_view(), name="profile_settings"),
    path("password/", UserPasswordChangeView.as_view(), name="password_change"),
]
