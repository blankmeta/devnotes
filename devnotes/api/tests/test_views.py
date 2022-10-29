from django.test import TestCase
from rest_framework.status import HTTP_201_CREATED
from rest_framework.test import APIClient

from notes.models import User, Theme, Note


class TestApi(TestCase):
    """ Test module for API """
    NUMBER_OF_THEMES = 4
    NUMBER_OF_NOTES = 1
    baseurl = '/api/v1/'

    def setUp(self):
        # Создаем авторизованный клиент
        auth_user_username = 'auth_user'
        auth_user_password = 'common_password'
        self.user = User.objects.create_user(username=auth_user_username,
                                             password=auth_user_password)
        self.authorized_client = APIClient()
        self.authorized_client.force_login(self.user)

        jwt_token = self.authorized_client.post(
            self.baseurl + 'jwt/create/',
            {
                'username': auth_user_username,
                'password': auth_user_password
            },
            format='json').data.get('access')

        self.authorized_client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + jwt_token)

        # Создаем 4 темы для пользователя
        for theme_count in range(1, 4):
            theme = Theme.objects.create(title=f'theme_{theme_count}')
            theme.author.add(self.user)

        self.test_theme = Theme.objects.create(title='test_theme')
        self.test_theme.author.add(self.user)

        # Создаем заметку
        self.test_note = Note.objects.create(title='test_title',
                                             text='test_text',
                                             theme=self.test_theme,
                                             author=self.user)

    def test_authenticated_user_create_new_theme(self):
        """Аутентифицированный пользователь может создать новую тему."""
        theme_title = 'new_theme'

        response_body = {
            'title': theme_title
        }
        response = self.authorized_client.post(self.baseurl + 'themes/',
                                               data=response_body,
                                               format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_authenticated_user_get_themes(self):
        """Аутентифицированный пользователь может получить свои темы."""
        response = self.authorized_client.get(self.baseurl + 'themes/')
        self.assertEqual(len(response.data), self.NUMBER_OF_THEMES)

    def test_authenticated_user_create_new_note(self):
        """Аутентифицированный пользователь может создать заметку."""
        response_body = {
            'theme': self.test_theme.slug,
            'title': 'note_title',
            'text': 'here is some text and code'
        }

        response = self.authorized_client.post(self.baseurl + 'notes/',
                                               data=response_body,
                                               format='json')
        self.assertEqual(response.status_code, HTTP_201_CREATED)

    def test_authenticated_user_get_notes(self):
        """Аутентифицированный пользователь может получить свои темы."""
        response = self.authorized_client.get(self.baseurl + 'notes/')

        self.assertEqual(len(response.data), self.NUMBER_OF_NOTES)
