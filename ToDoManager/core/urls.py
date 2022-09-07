from django.urls import path

from core.views import UserCreateView, login_user

urlpatterns = [
    path('signup/', UserCreateView.as_view()),
    path('login/', login_user, name='login'),
]
