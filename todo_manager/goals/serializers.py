from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import User
from goals.models import GoalsCategory, Goal, GoalComment


class UserSerializer(serializers.ModelSerializer):
    """
    Серелизатлор для пользователя
    """

    class Meta:
        model = User
        fields = ['id', "username", 'first_name', 'last_name', 'email']


class CreateGoalsCategorySerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания категории
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalsCategory
        read_only_fields = ['id', 'create', 'update', 'user']
        fields = "__all__"


class GoalsCategorySerializer(serializers.ModelSerializer):
    """
    Серелизатор для отображения, изменения и удаления категории
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = GoalsCategory
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "user", "category")


# -------------------------------------------------------------------------
class GoalCreateSerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания цели
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)

    class Meta:
        model = Goal
        fields = "__all__"

    def validate_category(self, value):
        if value.is_deleted:
            raise serializers.ValidationError('not allowed in deleted category')
        if value.user != self.context["request"].user:
            raise serializers.ValidationError("not owner of category")

    def create(self, validated_data):

        validated_data['category'] = get_object_or_404(GoalsCategory, pk=self.context['request'].data['category'])
        goal = Goal.objects.create(**validated_data)
        return goal


class GoalsSerializer(serializers.ModelSerializer):
    """
    Серелизатор для отображения, изменения и удаления цели
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class GoalCommentsCreateSerializer(serializers.ModelSerializer):
    created = serializers.DateTimeField(required=False)

    class Meta:
        model = GoalComment
        fields = "__all__"

    def create(self, validated_data):
        validated_data['goal'] = get_object_or_404(Goal, pk=self.context['request'].data['goal'])
        goal_comment = GoalComment.objects.create(**validated_data)
        return goal_comment


class GoalsCommentsSerializer(serializers.ModelSerializer):
    goal = serializers.SlugRelatedField(
        read_only=True,
        slug_field='title'
    )

    class Meta:
        model = GoalComment
        fields = "__all__"
        read_only_fields = ("id", "created", 'goal')
