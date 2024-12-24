from django.urls import path

from apps.health_check import views

app_name = "health-check"

urlpatterns = [
    path("", views.health_check_view, name="health-check"),
]
