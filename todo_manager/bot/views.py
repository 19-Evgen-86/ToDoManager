from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bot.models import TgUser
from bot.serialisers import VerifiedSerializer
from bot.tg.client import TgClient
from todo_manager import settings


class VerifiedView(GenericAPIView):

    model = TgUser
    permission_classes = [IsAuthenticated]
    serializer_class = VerifiedSerializer

    def patch(self, request, *args, **kwargs):
        serializer: VerifiedSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        tg_user: TgUser = serializer.validated_data['tg_user']
        tg_user.user = self.request.user
        tg_user.save(update_fields=('user',))

        instance: VerifiedSerializer = self.get_serializer(tg_user)
        TgClient(settings.TG_TOKEN).send_message(chat_id=tg_user.tg_chat, text="Verified success")
        return Response(instance.data)
