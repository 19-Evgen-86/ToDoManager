from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from goals.models import Board, GoalCategory, BoardParticipant
from tests.factories import UserFactory, BoardFactory, BoardParticipantFactory, GoalCategoryFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalCategoryAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def test_goals_category_create_view(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        data = {'title': 'test_category', 'board': board.id}
        response = self.client.post('/goals/goal_category/create', data)
        self.assertEqual(response.status_code, 201)
        goal_category: GoalCategory = GoalCategory.objects.last()
        expect_data = {'board': board.id,
                       'created': timezone.localtime(goal_category.created).isoformat(),
                       'id': goal_category.id,
                       'is_deleted': False,
                       'title': 'test_category',
                       'updated': timezone.localtime(goal_category.updated).isoformat()}
        self.assertEqual(response.json(), expect_data)

    def test_goals_category_create_not_participant(self):
        board: Board = BoardFactory()
        user = UserFactory()
        BoardParticipantFactory(board=board, user=user, role=BoardParticipant.Role.owner)
        data = {'title': 'test_category', 'board': board.id}
        response = self.client.post('/goals/goal_category/create', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_goals_category_retrieve(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        goal_category: GoalCategory = GoalCategoryFactory(user=self.user, board=board)
        response = self.client.get(reverse('category_view', kwargs={"pk": goal_category.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_goals_category_update(self):
        board: Board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        goal_category: GoalCategory = GoalCategoryFactory(user=self.user, board=board)
        response = self.client.patch(reverse('category_view', kwargs={"pk": goal_category.id}),
                                     {'title': 'new_title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        goal_category.refresh_from_db(fields=('title',))
        self.assertEqual(goal_category.title,'new_title')
