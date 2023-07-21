from rest_framework import serializers
from .models import Roteiro
from django.contrib.auth.models import User


# Responsável por serializar os dados do banco de dados para o formato JSON
class RoteiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roteiro
        exclude = ["texto_usuario", "resposta_chatgpt"]


class RoteiroListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Roteiro
        exclude = ["usuario"]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"],
            validated_data["email"],
            validated_data["password"],
        )
        return user
