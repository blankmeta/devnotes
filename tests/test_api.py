class TestApi:
    PREFIX = '/api/v1/'

    def test_get_notes(self, user_client, create_users_themes):
        """Аутентифицированный пользователь может получить свои темы"""
        url = self.PREFIX + 'themes/'
        response = user_client.get(url)
        assert response.data[0]['title'] == 'some_title'
