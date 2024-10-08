from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer[User]):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        return super().create(validated_data)
