import sentry_sdk
from django.db import connection
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check_view(_):
    try:
        connection.ensure_connection()
        return Response(status=status.HTTP_200_OK)
    except Exception as e:
        sentry_sdk.capture_exception(e)
        return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
