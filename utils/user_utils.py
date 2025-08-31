import re

from django.contrib.auth import get_user_model
from django.http.request import HttpRequest
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()


def get_connected_user(request: HttpRequest):
    """
    Get the current user from the request.

    :param request: HTTP request information of a endpoint
    :return: The user object if the user is authenticated, otherwise None.
    """
    header_token = request.META.get("HTTP_AUTHORIZATION", None)
    if not header_token or header_token == "Bearer":
        return None

    token = re.sub("Bearer ", "", header_token)
    if token == "undefined":
        return None

    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        return User.objects.get(id=user_id)

    except:
        return None
