from django.urls import path

from bot.views import verify

urlpatterns = [
    path('verify', verify, name='verify_code')
]
