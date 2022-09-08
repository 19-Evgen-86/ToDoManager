from django.urls import path

from core.views import UserCreateView, login_user, UserProfileView, UserUpdatePwdView

urlpatterns = [
    path('core/signup/', UserCreateView.as_view(),name='signup'),
    path('core/login/', login_user, name='login'),
    path('core/profile/', UserProfileView.as_view(), name='profile'),
    path('core/update_password/', UserUpdatePwdView.as_view(), name='new_password'),
]
