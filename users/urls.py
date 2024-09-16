from django.urls import path
from .views import UsersAPIView, LoginLogoutView


app_name = "user"
urlpatterns = [
    path("auth/login", LoginLogoutView.as_view({"post": "user_login"}), name="auth"),
    path("auth/logout", LoginLogoutView.as_view({"post": "user_logout"}), name="auth"),
    path("auth/refresh", LoginLogoutView.as_view({"post": "refresh_token"}), name="auth"),

    path('users', UsersAPIView.as_view({"post": "create", "get": "list"}), name='users'),
]
