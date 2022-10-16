# DJANGO_SETTINGS_MODULE=todo_manager.settings
from datetime import datetime

from django.test import TestCase

from core.models import User
from goals.models import GoalCategory, Board
from tests.factories import GoalCategoryFactory


class GoalCategoryModelTestCase(TestCase):

    def setUp(self) -> None:
        self.goal_category: GoalCategory = GoalCategoryFactory()

    def test_is_instance_field(self):
        self.assertIsInstance(self.goal_category.title, str)
        self.assertIsInstance(self.goal_category.is_deleted, bool)
        self.assertIsInstance(self.goal_category.user, User)
        self.assertIsInstance(self.goal_category.created, datetime)
        self.assertIsInstance(self.goal_category.updated, datetime)
        self.assertIsInstance(self.goal_category.board, Board)
