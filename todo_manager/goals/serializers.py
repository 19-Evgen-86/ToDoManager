from rest_framework import serializers

from core.models import User
from goals.models import GoalsCategory


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', "username", 'first_name', 'last_name','email']


class CreateGoalsCategorySerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsCategory
        read_only_fields = ['id', 'create', 'update', 'user']
        fields = "__all__"


class GoalsCategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalsCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user")

