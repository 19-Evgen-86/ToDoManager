from django.contrib import admin

from bot.models import TgUser


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'tg_user', 'tg_chat','verification_code')
    readonly_fields = ('tg_chat', 'verification_code')
