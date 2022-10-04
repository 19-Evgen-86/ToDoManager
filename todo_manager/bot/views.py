import json
import os

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from bot.models import TgUser
from bot.tg.client import TgClient
from bot.tg.dc import Message
from core.models import User


@require_http_methods(["PATCH"])
def verify(request):
    tg_client: TgClient = os.environ['tg_client']
    data = json.loads(request.body)
    verification_code = data['verification_code']
    res = tg_client.get_updates()
    tg_user: TgUser = TgUser.objects.filter(verification_code=verification_code)
    for item in res.result:
        if tg_user.tg_user:
            TgUser.objects.update(tg_user=item.message.from_.id, user=get_object_or_404(User, pk=data.user.id))
            tg_client.send_message(chat_id=item.message.chat.id, text='связка успешна')

    return HttpResponse(status=200)
