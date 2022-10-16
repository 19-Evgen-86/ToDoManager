# DJANGO_SETTINGS_MODULE=todo_manager.settings
from datetime import datetime

from django.test import TestCase

from core.models import User
from goals.models import Board, BoardParticipant
from tests.factories import BoardFactory, BoardParticipantFactory


class BoardModelTestCase(TestCase):

    def setUp(self) -> None:
        self.board: Board = BoardFactory()

    def test_is_instance_field(self):
        self.assertIsInstance(self.board.title, str)
        self.assertIsInstance(self.board.is_deleted, bool)
        self.assertIsInstance(self.board.created, datetime)
        self.assertIsInstance(self.board.updated, datetime)


class BoardParticipantModelTestCase(TestCase):

    def setUp(self) -> None:
        self.board_participant: BoardParticipant = BoardParticipantFactory()

    def test_is_instance_field(self):
        self.assertIsInstance(self.board_participant.created, datetime)
        self.assertIsInstance(self.board_participant.updated, datetime)
        self.assertIsInstance(self.board_participant.user, User)
        self.assertIsInstance(self.board_participant.board, Board)
        self.assertIsInstance(self.board_participant.role, int)
