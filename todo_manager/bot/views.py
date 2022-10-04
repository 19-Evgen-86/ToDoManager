from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from bot.models import TgUser
from bot.serializers import VerifySerializers


class Verify(UpdateAPIView):
    model = TgUser
    permission_classes = [IsAuthenticated]
    serializer_class = VerifySerializers

    def get_queryset(self):
        return TgUser.objects.all()
