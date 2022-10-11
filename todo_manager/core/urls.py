from django.urls import path

from core.views import UserCreateView, UserProfileView, UserUpdatePwdView, LoginUser

urlpatterns = [
    path('signup', UserCreateView.as_view(),name='signup'),
    path('login', LoginUser.as_view(), name='login'),
    path('profile', UserProfileView.as_view(), name='profile'),
    path('update_password', UserUpdatePwdView.as_view(), name='update_password'),
]
