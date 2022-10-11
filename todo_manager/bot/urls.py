from django.urls import path

from bot.views import VerifiedView

urlpatterns = [
    path('verify', VerifiedView.as_view(), name='verify_code')
]
