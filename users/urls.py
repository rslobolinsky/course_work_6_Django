from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import (UserCreateView, UserListView, UserLogin,
                         UserUpdateView, VerificationFailedView, activate,
                         generate_new_password)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", UserLogin.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),  # logout
    path("register/", UserCreateView.as_view(), name="register"),  # register
    path("activate/<str:uidb64>/<str:token>/", activate, name="activate"),  # activate
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path("users/", UserListView.as_view(), name="users_list"),
    path("verivication_failed/", VerificationFailedView.as_view(),name="email_confirmation_failed",),
    path("profile/", UserUpdateView.as_view(), name="profile"),
    path("profile/genpassword/", generate_new_password, name="generate_new_password"),
]
