from django.db.models.functions import Collate
from rest_framework.filters import OrderingFilter
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import CursorPagination


class AccountContextMixin:
    def get_serializer_context(self):
        request = self.request

        context = {
            "request": request,
            "format": self.format_kwarg,
            "view": self,
        }

        if request and request.user and request.user.account:
            context["account"] = request.user.account

        return context


class CreateModelWithAccountMixin(AccountContextMixin, CreateModelMixin):
    """
    Create a model instance with account context.
    """


class NaturalOrderingFilter(OrderingFilter):
    natural_fields = []

    def get_ordering(self, request, queryset, view):
        natural_ordering_fields = getattr(view, "natural_ordering_fields", None)
        ordering = super().get_ordering(request, queryset, view)

        for index, field in enumerate(ordering):
            if field in natural_ordering_fields:
                ordering[index] = Collate(field, "numeric")

        return ordering


class NaturalOrderingCursorPagination(CursorPagination):
    def _get_position_from_instance(self, instance, ordering):
        if isinstance(ordering[0], Collate):
            return ordering[0].source_expressions[0].name
        else:
            return super()._get_position_from_instance(instance, ordering)
