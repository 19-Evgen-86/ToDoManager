# DJANGO_SETTINGS_MODULE=todo_manager.settings
from datetime import datetime
from typing import Optional

from django.test import TestCase

from core.models import User
from goals.models import Goal
from tests.factories import GoalFactory


class GoalModelTestCase(TestCase):

    def setUp(self) -> None:
        self.goal: Goal = GoalFactory()

    def test_is_instance_field(self):
        self.assertIsInstance(self.goal.title, str)
        self.assertIsInstance(self.goal.is_deleted, bool)
        self.assertIsInstance(self.goal.user, User)
        self.assertIsInstance(self.goal.created, datetime)
        self.assertIsInstance(self.goal.updated, datetime)
        self.assertIsInstance(self.goal.due_date, str)
        self.assertIsInstance(self.goal.description, Optional[str])
        self.assertIsInstance(self.goal.status, int)
        self.assertIsInstance(self.goal.priority, int)
