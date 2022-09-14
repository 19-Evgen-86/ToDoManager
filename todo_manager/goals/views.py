from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.filters import GoalDateFilter
from goals.models import GoalsCategory, Goal, GoalComment
from goals.serializers import CreateGoalsCategorySerializer, GoalsCategorySerializer, GoalCreateSerializer, \
    GoalsSerializer, GoalCommentsCreateSerializer, GoalsCommentsSerializer


class CreateGoalsCategory(CreateAPIView):
    """
    View для создания категории задач
    """
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGoalsCategorySerializer


class GoalCategoryListView(ListAPIView):
    """
    View для отображения списка категорий
    """
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer
    pagination_class = LimitOffsetPagination

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
        return GoalsCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalsCategoryView(RetrieveUpdateDestroyAPIView):
    """
    View для отображения, изменения и удаления категории
    """
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer

    def get_queryset(self):
        return GoalsCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

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
    pagination_class = LimitOffsetPagination

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter, ]
    filterset_class = GoalDateFilter

    ordering = ["title"]
    search_fields = ['title']

    def get_queryset(self):
        return Goal.objects.filter(
            is_deleted=False
        )


class GoalsView(RetrieveUpdateDestroyAPIView):
    """
    View  для отображения, изменеия и удаления цели
    """
    model = Goal
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsSerializer

    def get_queryset(self):
        return Goal.objects.filter(
            is_deleted=False,
            user=self.request.user

        )

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
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = ['goal']
    ordering = ["-created"]

    def get_queryset(self):
        return GoalComment.objects.all()


class GoalsCommentView(RetrieveUpdateDestroyAPIView):
    model = GoalComment
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCommentsSerializer

    def get_queryset(self):
        return Goal.objects.all()
