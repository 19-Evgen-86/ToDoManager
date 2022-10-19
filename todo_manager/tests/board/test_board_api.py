from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from goals.models import Board, BoardParticipant
from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class BoardAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_board_create_view(self):
        data = {'title': 'test'}
        response = self.client.post('/goals/board/create', data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertEqual(response.data['title'], 'test')
        self.board: Board = BoardFactory()
        self.board_participant: BoardParticipant = BoardParticipantFactory(board=self.board, user=self.user,
                                                                           role=BoardParticipant.Role.owner)

    def test_board_list_view(self):
        boards: list(Board) = BoardFactory.create_batch(3)
        for board in boards:
            BoardParticipantFactory(board=board, user=self.user)
        self.assertEqual(BoardParticipant.objects.count(), 3)
        response = self.client.get(reverse('board_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)

    def test_retrieve_board(self):
        response = self.client.get(reverse('board_view', kwargs={'pk': self.board.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.board.title)

    def test_board_retrieve_not_participant(self):
        board = BoardFactory()
        board_participant = BoardParticipantFactory(board=board)
        response = self.client.get(reverse('board_view', kwargs={'pk': board.pk}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
