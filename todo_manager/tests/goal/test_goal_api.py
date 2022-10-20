from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from goals.models import GoalCategory, Board, BoardParticipant
from tests.factories import UserFactory, GoalCategoryFactory, GoalFactory, BoardFactory, BoardParticipantFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def test_goal_create_view(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.writer)
        category: GoalCategory = GoalCategoryFactory(board=board, user=self.user)
        data = {'title': 'test_category', 'category': category.pk, 'due_date': timezone.now()}
        response = self.client.post(reverse('goal_create'), data)
        self.assertEqual(response.status_code, 201)

    def test_create_not_participant(self):
        board: Board = BoardFactory()
        user = UserFactory()
        BoardParticipantFactory(board=board, user=user, role=BoardParticipant.Role.owner)
        category: GoalCategory = GoalCategoryFactory(board=board, user=self.user)

        data = {'title': 'test_category', 'category': category.pk, 'due_date': timezone.now()}
        response = self.client.post(reverse('goal_create'), data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'you are not a member of this board'})

    def test_create_participant_reader(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.reader)
        category: GoalCategory = GoalCategoryFactory(board=board, user=self.user)
        data = {'title': 'test_category', 'category': category.pk, 'due_date': timezone.now()}
        response = self.client.post(reverse('goal_create'), data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})
