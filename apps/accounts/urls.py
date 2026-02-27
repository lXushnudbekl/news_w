from django.urls import path
from .views import (
    dashboard_view,  logout_view, user_login_view, register_view, profile_update_view, user_password_change_view
)

urlpatterns = [
    path("", dashboard_view, name="dashboard"),
    path("login/", user_login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),
    path("settings/", profile_update_view, name="profile_settings"),
    path("password/", user_password_change_view, name="password_change"),
]
