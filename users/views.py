from django.shortcuts import render


from django.utils.translation import gettext_lazy as _
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from users.models import User
from users.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate, logout
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.pagination import PageNumberPagination
from django.contrib.auth.hashers import make_password


class LoginLogoutView(viewsets.ViewSet, TokenRefreshView):
    permission_classes = [AllowAny]

    def user_login(self, request):
        request_data = request.data.copy()
        email = request_data.get("email", "").lower()
        password = request_data.get("password", "")

        if not email or not password:
            return Response(
                {
                    "error": "Please provide required data.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        user = authenticate(request, email=email, password=password)
        if not user:
            return Response(
                {
                    "error": "Your authentication information is incorrect. Please try again.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        refresh = RefreshToken.for_user(user) 
        login_data = {
            "token": {
                "refreshToken": str(refresh),
                "accessToken": str(refresh.access_token),
            },
            "message": "Logged in successfully",
            "user": UserSerializer(user, context={'request': request}).data
        }
        return Response(login_data, status=status.HTTP_200_OK)

    def user_logout(self, request):
        try:
            logout(request)
            return Response({"message": "User logged out successfullly!"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error:", str(e))
            return Response(
                {"detail": "Invalid token."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def refresh_token(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                login_data = {
                    "token": {
                        "refreshToken": request.data["refresh"],
                        "accessToken": response.data["access"],
                    },
                    "message": "Logged in successfully.",
                }
                return Response(login_data, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "Login failed"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )
        except Exception as e:
            print("Error:", str(e))
            return Response(
                {"error": str(e)},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class UsersAPIView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        request_data = request.data
        request_data["password"] = make_password(request_data["password"])
        serializer = self.get_serializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
