import json
from typing import Dict

from django.contrib.auth import authenticate, login, logout, password_validation
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status, serializers
from rest_framework.exceptions import ValidationError
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


@csrf_exempt
@require_http_methods(["GET"])
def logout_user(request):
    logout(request)
    return JsonResponse({"message": "ok"}, status=200)


@method_decorator(ensure_csrf_cookie, name="dispatch")
class UserProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerialize

    def get_object(self):
        return self.request.user

    def delete(self, request, *args, **kwargs):
        logout(request)
        return Response("logout success", status=status.HTTP_204_NO_CONTENT)


class UserUpdatePwdView(UpdateAPIView):
    def update(self, request, *args, **kwargs):
        post_data: Dict = json.loads(request.body)
        old_password: str = post_data["old_password"]
        new_password: str = post_data["new_password"]

        user = get_object_or_404(User, pk=self.request.user.id)

        if not user.check_password(old_password):
            raise serializers.ValidationError("Passwords don't match.")

        try:
            password_validation.validate_password(new_password)
        except ValidationError as err:
            raise serializers.ValidationError(err)

        user.set_password(new_password)
        user.save()
        return Response("password update", status=200)
