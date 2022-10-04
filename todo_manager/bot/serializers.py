from rest_framework import serializers

from bot.models import TgUser


class VerifySerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = TgUser
        fields = ["verification_code", 'user']

    def update(self, instance, validated_data):
        if validated_data['verification_code'] == instance.verification_code:
            pass


        else:
            raise serializers.ValidationError("verification_code is not valid")

        return instance
