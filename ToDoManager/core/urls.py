from django.urls import path

from core.views import UserCreateView, login_user, UserProfileView, UserUpdatePwdView, logout_user

urlpatterns = [
    path('signup/', UserCreateView.as_view(),name='signup'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('update_password/', UserUpdatePwdView.as_view(), name='new_password'),
]
