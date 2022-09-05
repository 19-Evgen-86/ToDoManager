from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from core.models import User
from core.serializers import UserCreateSerialize


# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerialize

