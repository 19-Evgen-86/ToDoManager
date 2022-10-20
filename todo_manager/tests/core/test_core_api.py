import factory
from django.urls import reverse
from rest_framework import status

from rest_framework.test import APITestCase, APIClient

from core.models import User
from tests.factories import UserFactory


# DJANGO_SETTINGS_MODULE=todo_manager.settings
class CoreAPICreateUserTestCase(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('signup')

    def test_create_user(self):
        data = {'username': 'test_user', "password": "pwd12345", "password_repeat": "pwd12345"}

        response = self.client.post(self.url, data)
        user = User.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        user: User = User.objects.last()
        data = {'username': 'test_user', "password": "pwd12345", "password_repeat": "pwd12345"}
        expect_data = {
            'id': user.id,
            "username": 'test_user',
            'first_name': '',
            'last_name': '',
            'email': '',
        }
        self.assertEqual(response.json(), expect_data)
        self.assertNotEqual(user.password, 'pwd12345')
        self.assertTrue(user.check_password('pwd12345'))

    def test_valid_incorrect_email(self):
        data = {'username': 'test_user',
                "password": "pwd12345",
                "password_repeat": "pwd12345",
                'email': '111'
                }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['Enter a valid email address.']})

    def test_valid_short_password(self):
        data = {'username': 'test_user',
                "password": "R4@re",
                "password_repeat": "R4@re",
                }
        expect_data = {'password': ['This password is too short. It must contain at least 8 '
                                    'characters.'],
                       'password_repeat': ['This password is too short. It must contain at least 8 '
                                           'characters.']}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expect_data)

    def test_valid_dont_match_password(self):
        data = {'username': 'test_user',
                "password": "R4@reT65",
                "password_repeat": "R4@reT66",
                }
        expect_data = {'non_field_errors': ["Passwords don't match."]}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), expect_data)


class CoreAPILoginTestCase(APITestCase):

    def setUp(self) -> None:
        self.user: User = UserFactory(password='test4321')
        self.client = APIClient()
        self.url = reverse('login')

    def test_login(self):
        data = {'username': self.user.username, 'password': 'test4321'}
        expect_data = {'username': self.user.username}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect_data)
        self.assertNotEqual(response.cookies['sessionid'].value, '')

    def test_login_incorrect_username(self):
        response = self.client.post(self.url, {"username": "1111", 'password': "test4321"})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Incorrect authentication credentials.'})

    def test_login_incorrect_password(self):
        response = self.client.post(self.url, {"username": self.user.username, 'password': "incorrect_password"})

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'Incorrect authentication credentials.'})


class CoreAPIProfileTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.client = APIClient()
        self.url = reverse('profile')
        self.client.force_login(self.user)

    def test_logout(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.cookies['sessionid'].value, '')

    def test_get_profile_user(self):
        response = self.client.get(self.url)
        expect_data = {'email': self.user.email,
                       'first_name': self.user.first_name,
                       'id': self.user.id,
                       'last_name': self.user.last_name,
                       'username': self.user.username}
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect_data)

    def test_update_profile_user(self):
        self.assertEqual(self.user.first_name, '')
        response = self.client.patch(self.url, {'first_name': 'sky.pro'})

        expect_data = {'email': self.user.email,
                       'first_name': 'sky.pro',
                       'id': self.user.id,
                       'last_name': self.user.last_name,
                       'username': self.user.username}
        self.user.refresh_from_db(fields=('first_name',))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), expect_data)
        self.assertEqual(self.user.first_name, 'sky.pro')


class CoreAPIUpdatePasswordTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = UserFactory(password='test4321')
        self.client = APIClient()
        self.url = reverse('update_password')

    def test_auth_required(self):
        data = {
            'old_password': 'test_old_password',
            'new_password': 'test_new_password'
        }
        response = self.client.patch(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # def test_incorrect_old_password(self):
    #     self.client.force_login(self.user)
    #
    #     data = {
    #         'old_password': 'test_old_password',
    #         'new_password': 'test_new_password',
    #     }
    #     response = self.client.patch(self.url, data)
    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertEqual(response.json(), 2)
