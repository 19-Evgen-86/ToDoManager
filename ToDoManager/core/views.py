from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from ToDoManager.core.models import User


# Create your views here.
class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerialize