from rest_framework_simplejwt.tokens import RefreshToken


class JWTAuthService:
    """JWT Service for authentication operations"""

    def generate_tokens(self, user):
        """Generate JWT tokens for user"""

        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    def blacklist_token(self, refresh_token):
        """Blacklist refresh token"""

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return True

        except Exception:
            return False
