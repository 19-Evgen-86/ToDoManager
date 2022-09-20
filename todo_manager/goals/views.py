from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import GoalCategory, Goal, GoalComment, Board
from goals.permissions import BoardPermissions
from goals.serializers import CreateGoalsCategorySerializer, GoalsCategorySerializer, GoalCreateSerializer, \
    GoalsSerializer, GoalCommentsCreateSerializer, GoalsCommentsSerializer, BoardSerializer


class CreateGoalsCategory(CreateAPIView):
    """
    View для создания категории задач
    """
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGoalsCategorySerializer


class GoalCategoryListView(ListAPIView):
    """
    View для отображения списка категорий
    """
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer

    filter_backends = [
        # фильтр соритровки
        filters.OrderingFilter,
        # фильтр поиска
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ['title']

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(is_deleted=False, user=self.request.user.id)


class GoalsCategoryView(RetrieveUpdateDestroyAPIView):
    """
    View для отображения, изменения и удаления категории
    """
    model = GoalCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer

    def get_queryset(self):
        return GoalCategory.objects.select_related('user').filter(is_deleted=False, user=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        goals = Goal.objects.filter(category=instance.id).all()
        for goal in goals:
            goal.is_deleted = True
            goal.save()
        instance.save()

        return instance


class GoalCreateView(CreateAPIView):
    """
    View для создания цели
    """
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCreateSerializer


class GoalsListView(ListAPIView):
    """
    View для отображения списка целей
    """
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsSerializer

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter, ]
    filterset_class = GoalDateFilter

    ordering = ["title"]
    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(is_deleted=False, user=self.request.user.id)


class GoalsView(RetrieveUpdateDestroyAPIView):
    """
    View  для отображения, изменеия и удаления цели
    """
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsSerializer

    def get_queryset(self):
        return Goal.objects.select_related('user').filter(is_deleted=False, user=self.request.user.id)

    def perform_destroy(self, instance):
        instance.is_deleted = True

        instance.save()
        return instance


class GoalCommentsCreateView(CreateAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalCommentsCreateSerializer


class GoalsCommentListView(ListAPIView):
    """
    View для отображения списка комментариев
    """
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCommentsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.OrderingFilter]
    search_fields = ['text']
    filterset_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.all()


class GoalsCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCommentsSerializer

    def get_queryset(self):
        return GoalComment.objects.all()


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=Goal.Status.archived
            )
        return instance