# DJANGO_SETTINGS_MODULE=todo_manager.settings
from datetime import datetime

from django.test import TestCase

from core.models import User
from goals.models import GoalComment, Goal
from tests.factories import GoalCommentFactory


class GoalCommentTestCase(TestCase):

    def setUp(self) -> None:
        self.goal_comment: GoalComment = GoalCommentFactory()

    def test_is_instance_field(self):
        self.assertIsInstance(self.goal_comment.user, User)
        self.assertIsInstance(self.goal_comment.goal, Goal)
        self.assertIsInstance(self.goal_comment.text, str)
        self.assertIsInstance(self.goal_comment.created, datetime)
        self.assertIsInstance(self.goal_comment.updated, datetime)
