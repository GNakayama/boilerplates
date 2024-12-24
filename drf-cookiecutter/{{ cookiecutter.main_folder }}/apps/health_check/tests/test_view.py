import pytest
from django.urls import reverse

from conftest import client


@pytest.mark.django_db
def test_health_check():
    response = client("get", reverse("health-check-api:health-check"))

    assert response.status_code == 200


@pytest.mark.django_db
def test_health_check_exception(mocker):
    mocked_connection = mocker.patch("apps.health_check.views.health_check.connection")
    mocked_sentry = mocker.patch("apps.health_check.views.health_check.sentry_sdk")

    mocked_connection.ensure_connection = Exception()
    client("get", reverse("health-check-api:health-check"))

    mocked_sentry.capture_exception.assert_called()
