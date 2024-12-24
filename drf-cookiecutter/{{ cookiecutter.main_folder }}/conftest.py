from types import SimpleNamespace

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken


def client(method, *args, **kwargs):
    api_client = APIClient()

    fn = getattr(api_client, method)

    if "format" not in kwargs:
        kwargs["format"] = "json"

    token = kwargs.pop("token", None)

    if token:
        api_client.credentials(HTTP_AUTHORIZATION="Bearer {}".format(token))

    apikey = kwargs.pop("apikey", None)

    if apikey:
        api_client.credentials(HTTP_AUTHORIZATION="Api-Key {}".format(apikey))

    return fn(*args, **kwargs)


def public_client(method, *args, **kwargs):
    return client(method, *args, **kwargs)


def build_token(uuid, account_uuid):
    user = SimpleNamespace()
    user.uuid = uuid
    refresh = RefreshToken.for_user(user)
    refresh["account"] = account_uuid
    refresh["email"] = "logged_user@example.com"
    refresh["first_name"] = "John"
    refresh["last_name"] = "Doe"

    return str(refresh.access_token)
