from rest_framework.validators import UniqueTogetherValidator


class UniqueTogetherWithAccountValidator(UniqueTogetherValidator):
    def filter_queryset(self, attrs, queryset, serializer):
        queryset = queryset.filter(account=serializer.context["account"])

        return super().filter_queryset(attrs, queryset, serializer)
