from django.urls import path

from core.views import UserCreateView, login_user,UserProfileView

urlpatterns = [
    path('signup/', UserCreateView.as_view(),name='signup'),
    path('login/', login_user, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
