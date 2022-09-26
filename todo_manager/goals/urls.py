from django.urls import path

from goals.views import CreateGoalsCategory, GoalCategoryListView, GoalsCategoryView, GoalCreateView, GoalsView, \
    GoalsListView, GoalCommentsCreateView, GoalsCommentListView, GoalsCommentView, BoardListView, BoardView, \
    BoardCreateView

urlpatterns = [
    path('goal_category/create', CreateGoalsCategory.as_view(), name='create_category'),
    path('goal_category/list', GoalCategoryListView.as_view(), name='category_list'),
    path('goal_category/<pk>', GoalsCategoryView.as_view(), name='category_view'),
    path('goal/create', GoalCreateView.as_view(), name='goal_create'),
    path('goal/list', GoalsListView.as_view(), name='goal_list'),
    path('goal/<pk>', GoalsView.as_view(), name='goal_view'),
    path('goal_comment/create', GoalCommentsCreateView.as_view(), name='goal_comment_create'),
    path('goal_comment/list', GoalsCommentListView.as_view(), name='goal_comment_list'),
    path('goal_comment/<pk>', GoalsCommentView.as_view(), name='goal_comment_view'),
    path('board/create',BoardCreateView.as_view(),  name='board_create'),
    path('board/list', BoardListView.as_view(), name='board_list'),
    path('board/<pk>', BoardView.as_view(), name='board_view'),

]
