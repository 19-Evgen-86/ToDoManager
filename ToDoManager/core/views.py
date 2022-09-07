from django.contrib.auth import authenticate, login
from django.shortcuts import render
from rest_framework.generics import CreateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from core.models import User
from core.serializers import UserCreateSerialize, UserDeleteSerialize


# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerialize


def login_user(request):
    ...


class UserDetailView(RetrieveAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UserDeleteSerialize


class UserUpdateView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
