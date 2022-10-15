from django.contrib.auth import logout, login
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerialize, UserUpdateSerialize, \
    UserUpdatePwdSerialize, LoginSerialize


# Create your views here.
class UserCreateView(CreateAPIView):
    """
        Создание пользователя
    """
    serializer_class = UserCreateSerialize


class LoginUser(GenericAPIView):
    """
        Авторизация пользователя
    """
    serializer_class = LoginSerialize

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return Response(serializer.data)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """
       Обновление данных пользователя
    """
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerialize

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserUpdatePwdView(UpdateAPIView):
    """
        Обновление пароля пользователя
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdatePwdSerialize

    def get_object(self):
        return self.request.user
