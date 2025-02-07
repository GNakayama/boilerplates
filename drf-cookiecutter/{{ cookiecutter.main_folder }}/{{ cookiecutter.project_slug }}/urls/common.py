"""{{ cookiecutter.project_slug }} URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

admin.autodiscover()

urlpatterns = [
    path(r"admin/", admin.site.urls),
    path(
        "health-check/",
        include("apps.health_check.urls", namespace="health-check-api"),
    ),
    path(
        "public/",
        include("{{ cookiecutter.project_slug }}.urls.public_api"),
    ),
    re_path(r"^", include("{{ cookiecutter.project_slug }}.urls.api")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path(
            "openapi/",
            get_schema_view(
                title="Internal API docs",
                description="Documentation for internal API",
                public=True,
                patterns=[
                    re_path(r"^", include("{{ cookiecutter.project_slug }}.urls.common")),
                ],
            ),
            name="openapi-schema",
        ),
        path(
            "docs/",
            TemplateView.as_view(
                template_name="docs.html",
                extra_context={"schema_url": "openapi-schema"},
            ),
            name="docs",
        ),
    ]
