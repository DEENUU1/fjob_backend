from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication class extending the default JWTAuthentication.

    Overrides the authenticate method to handle token extraction from both headers and cookies.

    Methods:
    - authenticate(self, request): Authenticates the user based on the provided token.

    Attributes:
    - None
    """

    def authenticate(self, request):
        """
        Authenticates the user based on the provided token from headers or cookies.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Tuple[User, Token]: A tuple containing the user and the validated token, or None if authentication fails.
        """
        try:
            header = self.get_header(request)

            if header is None:
                raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
            else:
                raw_token = self.get_raw_token(header)

            if raw_token is None:
                return None

            validated_token = self.get_validated_token(raw_token)

            return self.get_user(validated_token), validated_token
        except:
            return None
