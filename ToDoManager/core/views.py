import json
from typing import Dict

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserCreateSerialize, UserDeleteSerialize


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


class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeleteSerialize


class UserUpdateView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        logout(request)
