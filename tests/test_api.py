from rest_framework import status


class TestApi:
    PREFIX = '/api/v1/'
    BASE_URL = PREFIX + 'themes/'

    def test_non_auth_get_themes(self, client):
        """Неаутентифицированный пользователь не может получить свой список тем."""
        response = client.get(self.BASE_URL)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            'Неаутентифицированный пользователь должен получать 401_UNAUTHORIZED при попытке получить список своих тем.'
        )

    def test_success_get_themes(self, user_client):
        """Аутентифицированный пользователь получает 200 при получении списка тем."""
        response = user_client.get(self.BASE_URL)

        assert response.status_code == status.HTTP_200_OK, (
            'Аутентифицированный пользователь должен получать 200_OK при запросе списка тем.'
        )

    def test_get_themes(self, user_client, create_users_themes):
        """Аутентифицированный пользователь может получить свои темы."""
        response = user_client.get(self.BASE_URL)

        test_data = response.json()[0]

        assert test_data['title'] == 'some_title', (
            'Аутентифицированный пользователь получает список своих тем.'
        )
