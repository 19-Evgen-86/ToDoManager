from typing import List

from django.test import TestCase
from django.utils import timezone

from goals.models import Board, BoardParticipant, GoalCategory, Goal, GoalComment
from goals.serializers import BoardListSerializer, BoardSerializer, BoardParticipantSerializer, \
    CreateGoalsCategorySerializer, GoalCreateSerializer, GoalCommentsCreateSerializer, BoardCreateSerializer
from tests.factories import BoardFactory, BoardParticipantFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings


class CreateSerializersTestCase(TestCase):
    def test_create_goals_category_serializer(self):
        """
        CreateGoalsCategorySerializer
        """
        goal_category: GoalCategory = GoalCategoryFactory()
        data = CreateGoalsCategorySerializer(goal_category).data
        ex_data = {"id": goal_category.id, 'is_deleted': False, "title": goal_category.title,
                   "board": goal_category.board.id}
        self.assertEqual(ex_data, data)

    def test_create_goal_serializer(self):
        """
        GoalCreateSerializer
        """
        goal: Goal = GoalFactory()
        data = GoalCreateSerializer(goal).data
        ex_data = {'id': goal.id, 'created': goal.created, 'updated': goal.updated,
                   'title': goal.title, 'description': goal.description, 'status': goal.status,
                   'priority': goal.priority,
                   'due_date': goal.due_date,
                   'is_deleted': False, 'category': goal.category.id}
        self.assertEqual(ex_data, data)

    def test_create_goal_comments_serializer(self):
        """
        GoalCommentsCreateSerializer
        """
        goal_comment: GoalComment = GoalCommentFactory()
        data = GoalCommentsCreateSerializer(goal_comment).data
        ex_data = {'id': goal_comment.id, 'created': goal_comment.created, 'updated': goal_comment.updated,
                   'text': goal_comment.text, 'goal': goal_comment.goal.id}
        self.assertEqual(ex_data, data)

    def test_create_board_serializer(self):
        """
        BoardCreateSerializer
        """
        board: Board = BoardFactory()
        data = BoardCreateSerializer(board).data
        ex_data = {'id': board.id, 'created': board.created, 'updated': board.updated, 'title': board.title,
                   'is_deleted': False}
        self.assertEqual(ex_data, data)





