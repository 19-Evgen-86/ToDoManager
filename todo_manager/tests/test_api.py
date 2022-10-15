from django.utils import timezone
from rest_framework.test import APITestCase, APIClient

from tests.factories import UserFactory, BoardFactory, GoalCategoryFactory, GoalFactory, GoalCommentFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class CreateViewTestCase(APITestCase):
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

    def test_goals_category_create_view(self):
        board = BoardFactory()
        data = {'title': 'test_category', 'board': board.id}
        response = self.client.post('/goals/goal_category/create', data)
        self.assertEqual(response.status_code, 201)

    def test_goal_create_view(self):
        category = GoalCategoryFactory()
        data = {'title': 'test_category', 'board': category.id, 'due_date': timezone.now()}
        response = self.client.post('/goals/goal/create', data)
        self.assertEqual(response.status_code, 201)

    def test_goal_comment_create_view(self):
        goal = GoalFactory()
        data = {'text': 'test_comment', 'board': goal.id}
        response = self.client.post('/goals/goal_comment/create', data)
        self.assertEqual(response.status_code, 201)


class ListViewTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.client.force_login(self.user)
        self.goals = GoalFactory.create_batch(2)
        self.boards = BoardFactory.create_batch(2)
        self.goal_categories = GoalCategoryFactory.create_batch(2)
        self.goal_comments = GoalCommentFactory.create_batch(2)

    def tearDown(self) -> None:
        self.client.logout()

    def test_board_list_view(self):
        response = self.client.get('/goals/board/list')
        self.assertEqual(response.status_code, 200)

    def test_goals_category_list_view(self):
        response = self.client.get('/goals/goal_category/list')
        self.assertEqual(response.status_code, 200)

    def test_goal_list_view(self):
        response = self.client.get('/goals/goal/list')
        self.assertEqual(response.status_code, 200)

    def test_goal_comment_list_view(self):
        response = self.client.get('/goals/goal_comment/list')
        self.assertEqual(response.status_code, 200)
