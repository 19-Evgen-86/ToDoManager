from django.urls import path

from goals.views import CreateGoalsCategory, GoalCategoryListView, GoalsCategoryView

urlpatterns = [
    path('goal_category/create', CreateGoalsCategory.as_view(), name='create_category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalsCategoryView.as_view(), name='category_view')
]
