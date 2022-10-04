from django.urls import path

from bot.management.commands.runbot import verify

urlpatterns = [
    path('verify', verify, name='verify_code')
]
