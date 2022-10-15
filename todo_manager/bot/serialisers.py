from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class VerifiedSerializer(serializers.ModelSerializer):
    """
        сериализатор для верефикации пользователя бота
    """
    verification_code = serializers.CharField(write_only=True)
    chat_id = serializers.SlugField(source='tg_chat', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_user', 'chat_id', 'verification_code')
        read_only_field = ('chat_id', 'user', 'tg_user')

    def validate(self, attrs):
        verification_code = attrs.get('verification_code')
        user = TgUser.objects.filter(verification_code=verification_code).first()
        if not user:
            raise ValidationError({"verification_code": "code is incorrect"})

        attrs['tg_user'] = user
        return attrs
