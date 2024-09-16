from django.urls import path
from .views import SessionAPIView


app_name = "session"
urlpatterns = [
    path('session', SessionAPIView.as_view({"post": "create", "get": "list"}), name='session'),
    path("session/<str:pk>", SessionAPIView.as_view({"delete": "destroy", "get": "retrieve"}), name="session")
]
