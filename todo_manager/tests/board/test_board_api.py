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

    def test_board_create_view(self):
        data = {'title': 'test'}
        response = self.client.post('/goals/board/create', data)
        self.assertEqual(response.status_code, 201)
        board: Board = Board.objects.last()

        expect_data = {
            'id': board.id,
            'is_deleted': False,
            'title': 'test',
            'updated': timezone.localtime(board.updated).isoformat(),
            'created': timezone.localtime(board.created).isoformat()}

        self.assertEqual(response.json(), expect_data)

    def test_board_list_view(self):
        boards: list[Board] = BoardFactory.create_batch(3)
        for board in boards:
            BoardParticipantFactory(board=board, user=self.user)
        self.assertEqual(BoardParticipant.objects.count(), 3)
        response = self.client.get(reverse('board_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), list)
        self.assertEqual(len(response.json()), 3)

    def test_retrieve_board(self):
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        response = self.client.get(reverse('board_view', kwargs={'pk': board.pk}))
        self.assertEqual(response.status_code, 200)

    def test_retrieve_update_board(self):
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)

        response = self.client.put(reverse('board_view', kwargs={'pk': board.pk}),
                                   {"title": "new_title", 'participants': []})
        self.assertEqual(response.status_code, 200)
        board.refresh_from_db(fields=('title',))
        self.assertEqual(board.title, 'new_title')

    def test_retrieve_update_board_reader(self):
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.reader)

        response = self.client.put(reverse('board_view', kwargs={'pk': board.pk}),
                                   {"title": "new_title", 'participants': []})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
