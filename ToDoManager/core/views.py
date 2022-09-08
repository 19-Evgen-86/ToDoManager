import json
from typing import Dict

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import User
from core.serializers import UserCreateSerialize, UserDetailSerialize, UserUpdateSerialize, \
    UserUpdatePwdSerialize


# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerialize


@csrf_exempt
@require_http_methods(["POST"])
def login_user(request):
    post_data: Dict = json.loads(request.body)
    username: str = post_data["username"]
    password: str = post_data["password"]
    user: User = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"message": "ok"}, status=200)
    else:
        return JsonResponse({"message": "User not found! Check Username or Password"}, status=200)

@method_decorator(ensure_csrf_cookie,name="dispatch")
class UserProfileView(RetrieveUpdateDestroyAPIView):


    def get(self, request, *args, **kwargs):
        """
        Вывод профиля пользователя
        """

        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserDetailSerialize(user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """
        Полное обновдление данных пользователя
        """
        data = json.loads(request.body)
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserUpdateSerialize(user, data=data)

        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        """
        Частичное обновление данных пользователя
        """

        data = json.loads(request.body)
        user = get_object_or_404(User, pk=request.user.id)
        serializer = UserUpdateSerialize(user, data=data)

        return Response(serializer.data)


    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response("logout success", status=status.HTTP_204_NO_CONTENT)


class UserUpdatePwdView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdatePwdSerialize


