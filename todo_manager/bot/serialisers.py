from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from bot.models import TgUser


class VerifiedSerializer(serializers.ModelSerializer):
    verification_code = serializers.CharField(write_only=True)
    tg_chat = serializers.SlugField(source='tg_chat', read_only=True)

    class Meta:
        model = TgUser
        fields = ('tg_user', 'tg_chat', 'verification_code')
        read_only_field = ('tg_chat', 'user', 'tg_user')

    def validate(self, attrs):
        verification_code = attrs.get['verification_code']
        user = TgUser.objects.filters(verification_code=verification_code).first()
        if not user:
            raise ValidationError({"verification_code": "code is incorrect"})

        attrs['tg_user'] = user
        return attrs
