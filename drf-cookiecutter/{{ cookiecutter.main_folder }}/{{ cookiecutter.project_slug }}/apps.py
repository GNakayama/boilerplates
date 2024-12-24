from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = "{{ cookiecutter.project_slug }}"

    def ready(self):
        pass
