from django.conf import settings
from djoser.social.views import ProviderAuthView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)


class CustomProviderAuthView(ProviderAuthView):
    """
    Custom view for handling authentication with third-party providers.

    Overrides the post method to set cookies for access and refresh tokens.

    Methods:
    - post(self, request, *args, **kwargs): Handles the HTTP POST request for authentication.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for authentication.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The HTTP response object.
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == 201:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens.

    Overrides the post method to set cookies for access and refresh tokens.

    Methods:
    - post(self, request, *args, **kwargs): Handles the HTTP POST request for obtaining tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for obtaining tokens.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The HTTP response object.
        """
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')
            refresh_token = response.data.get('refresh')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )
            response.set_cookie(
                'refresh',
                refresh_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT tokens.

    Overrides the post method to set a new access token cookie.

    Methods:
    - post(self, request, *args, **kwargs): Handles the HTTP POST request for refreshing tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for refreshing tokens.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The HTTP response object.
        """
        refresh_token = request.COOKIES.get('refresh')

        if refresh_token:
            request.data['refresh'] = refresh_token

        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            access_token = response.data.get('access')

            response.set_cookie(
                'access',
                access_token,
                max_age=settings.AUTH_COOKIE_MAX_AGE,
                path=settings.AUTH_COOKIE_PATH,
                secure=settings.AUTH_COOKIE_SECURE,
                httponly=settings.AUTH_COOKIE_HTTP_ONLY,
                samesite=settings.AUTH_COOKIE_SAMESITE
            )

        return response


class CustomTokenVerifyView(TokenVerifyView):
    """
    Custom view for verifying JWT tokens.

    Overrides the post method to use the access token from cookies.

    Methods:
    - post(self, request, *args, **kwargs): Handles the HTTP POST request for verifying tokens.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for verifying tokens.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The HTTP response object.
        """
        access_token = request.COOKIES.get('access')

        if access_token:
            request.data['token'] = access_token

        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    """
    View for handling user logout.

    Overrides the post method to delete access and refresh token cookies.

    Methods:
    - post(self, request, *args, **kwargs): Handles the HTTP POST request for user logout.
    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request for user logout.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The HTTP response object.
        """
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie('access')
        response.delete_cookie('refresh')

        return response
