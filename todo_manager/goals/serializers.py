from django.shortcuts import get_object_or_404
from rest_framework import serializers

from core.models import User
from core.serializers import UserUpdateSerialize
from goals.models import GoalCategory, Goal, GoalComment, Board, BoardParticipant


class CreateGoalsCategorySerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания категории
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalCategory
        read_only_fields = ['id', 'created', 'updated', 'user']
        fields = "__all__"


class GoalsCategorySerializer(serializers.ModelSerializer):
    """
    Серелизатор для отображения, изменения и удаления категории
    """
    user = UserUpdateSerialize(read_only=True)

    class Meta:
        model = GoalCategory
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

        validated_data['category'] = get_object_or_404(GoalCategory, pk=self.context['request'].data['category'])
        goal = Goal.objects.create(**validated_data)
        return goal


class GoalsSerializer(serializers.ModelSerializer):
    """
    Серелизатор для отображения, изменения и удаления цели
    """
    user = UserUpdateSerialize(read_only=True)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")


class GoalCommentsCreateSerializer(serializers.ModelSerializer):
    """
        Серелизатор для создания коммнентария
    """
    created = serializers.DateTimeField(required=False)
    updated = serializers.DateTimeField(required=False)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = GoalComment
        fields = "__all__"

    def create(self, validated_data):
        # validated_data['user'] = get_object_or_404(User, pk=self.context['request'].user.id)
        validated_data['goal'] = get_object_or_404(Goal, pk=self.context['request'].data['goal'])
        goal_comment = GoalComment.objects.create(**validated_data)
        return goal_comment


class GoalsCommentsSerializer(serializers.ModelSerializer):
    """
    Серелизатор для отображения, изменения и удаления комментария
    """
    user = UserUpdateSerialize(read_only=True)
    goal = serializers.SlugRelatedField(read_only=True, slug_field="title")

    class Meta:
        model = GoalComment
        fields = ["id", "text", "goal", 'user']


class BoardCreateSerializer(serializers.ModelSerializer):
    """
    Серелизатор для создания доски
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        read_only_fields = ("id", "created", "updated")
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data.pop("user")
        board = Board.objects.create(**validated_data)
        BoardParticipant.objects.create(
            user=user, board=board, role=BoardParticipant.Role.owner
        )
        return board


class BoardParticipantSerializer(serializers.ModelSerializer):
    """
    Серелизатор для работы с участниками доски

    """
    role = serializers.ChoiceField(
        required=True, choices=BoardParticipant.editable_choices
    )
    user = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.all()
    )

    class Meta:
        model = BoardParticipant
        fields = "__all__"
        read_only_fields = ("id", "created", "updated", "board")


class BoardSerializer(serializers.ModelSerializer):
    """
    Серелизатор для работы доской
    """
    participants = BoardParticipantSerializer(many=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Board
        fields = "__all__"
        read_only_fields = ("id", "created", "updated")

    def update(self, instance, validated_data):
        # ваш код для работы с участниками
        return instance
