import functools

from rest_framework import status
from rest_framework.response import Response

from utils.user_utils import get_connected_user


def check_user_is_connected(api_func):
    """Decorator to check if the user who is making the request is connected."""

    @functools.wraps(api_func)
    def wrapper(*args, **kwargs):
        request = args[1]
        connected_user = get_connected_user(request)
        if not connected_user:
            return Response(
                data={"error": "You are not connected !"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return api_func(*args, **kwargs)

    return wrapper
