from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from goals.models import BoardParticipant, GoalComment
from tests.factories import UserFactory, GoalFactory, BoardParticipantFactory, BoardFactory, GoalCategoryFactory, \
    GoalCommentFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class GoalCommentAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)

    def tearDown(self) -> None:
        self.client.logout()

    def test_goal_comment_create_view(self):
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        category = GoalCategoryFactory(board=board, user=self.user)
        goal = GoalFactory(user=self.user, category=category)
        data = {'text': 'test_comment', 'goal': goal.id}

        response = self.client.post(reverse('goal_comment_create'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_goal_comment_retrieve(self):
        board = BoardFactory()
        BoardParticipantFactory(board=board, user=self.user, role=BoardParticipant.Role.owner)
        category = GoalCategoryFactory(board=board, user=self.user)
        goal = GoalFactory(user=self.user, category=category)
        goal_comments: GoalComment = GoalCommentFactory(goal=goal, user=self.user)
        response = self.client.get(reverse('goal_comment_view', kwargs={'pk': goal_comments.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

