import re

from django.contrib.auth import get_user_model
from rest_framework import serializers, validators
from rest_framework.exceptions import ValidationError

User = get_user_model()


class CustomUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        validators=[
            validators.UniqueValidator(queryset=User.objects.all()),
        ],
        max_length=254,
    )

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'bio',
            'role',
        )


class CustomUserCreationSerializer(serializers.Serializer):

    username = serializers.CharField(
        required=True,
        max_length=150,
    )
    email = serializers.EmailField(required=True, max_length=50)

    def validate_username(self, data):
        username = data
        email = self.initial_data.get('email')
        if username == 'me':
            raise ValidationError(f'Логин {username} недоступен')
        if not re.match(r'^[\w.@+-]+$', username):
            raise serializers.ValidationError('Некорректный формат логина')
        if (
            User.objects.filter(username=username)
            and not User.objects.filter(email=email)
        ) or (
            User.objects.filter(email=email)
            and not User.objects.filter(username=username)
        ):
            raise serializers.ValidationError(
                'Пользователь зарегистрирован с другим логином или почтой'
            )
        return data


class CodeConfirmSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    extra_kwargs = {
        'confirmation_code': {'required': True},
        'username': {'required': True},
    }
