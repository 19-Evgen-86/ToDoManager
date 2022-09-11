from django.urls import path

from core.views import UserCreateView, login_user, UserProfileView, UserUpdatePwdView, logout_user

urlpatterns = [
    path('core/signup', UserCreateView.as_view(),name='signup'),
    path('core/login', login_user, name='login'),
    path('core/logout', logout_user, name='logout'),
    path('core/profile', UserProfileView.as_view(), name='profile'),
    path('core/update_password', UserUpdatePwdView.as_view(), name='new_password'),
]
