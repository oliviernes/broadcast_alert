"""Map URL patterns to view function"""
from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("my_account/", views.my_account, name="my_account"),
    path("login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path(
        "reset_password/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset.html"
        ),
        name="reset_password",
    ),
    path(
        "reset_password_sent/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_sent.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset_password/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_form.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset_password_complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_complete",
    ),
]
