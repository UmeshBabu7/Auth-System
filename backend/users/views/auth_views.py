from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import (
    CustomUserSerializer,
    RegisterUserSerializer,
    LoginUserSerializer,
)

COOKIE_SETTINGS = {
    "httponly": True,
    "secure": True,
    "samesite": "None",
}


class UserRegistrationView(CreateAPIView):
    serializer_class = RegisterUserSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data
        refresh = RefreshToken.for_user(user)

        response = Response(
            {"user": CustomUserSerializer(user).data}, status=status.HTTP_200_OK
        )
        response.set_cookie(
            key="access_token", value=str(refresh.access_token), **COOKIE_SETTINGS
        )
        response.set_cookie(key="refresh_token", value=str(refresh), **COOKIE_SETTINGS)
        return response


class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token:
            try:
                RefreshToken(refresh_token).blacklist()
            except Exception as e:
                return Response(
                    {"error": f"Error invalidating token: {str(e)}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        response = Response(
            {"message": "Successfully logged out!"}, status=status.HTTP_200_OK
        )
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")
        return response
