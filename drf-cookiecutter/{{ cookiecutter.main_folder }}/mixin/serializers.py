from rest_framework.serializers import ModelSerializer


class ModelWithAccountSerializer(ModelSerializer):
    def validate(self, attrs):
        attrs["account"] = self.context["account"]

        return super().validate(attrs)

    def create(self, validated_data):
        validated_data["account"] = self.context["account"]

        return super().create(validated_data)
