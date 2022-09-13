from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from goals.models import GoalsCategory
from goals.serializers import CreateGoalsCategorySerializer, GoalsCategorySerializer


class CreateGoalsCategory(CreateAPIView):
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = CreateGoalsCategorySerializer


class GoalCategoryListView(ListAPIView):
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
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
    model = GoalsCategory
    permission_classes = [IsAuthenticated]
    serializer_class = GoalsCategorySerializer

    def get_queryset(self):
        return GoalsCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance
