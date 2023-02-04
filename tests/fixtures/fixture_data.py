import pytest

from notes.models import Theme


@pytest.fixture
def create_users_themes(user):
    another_theme = Theme.objects.create(title='some_title')
    another_theme.author.add(user.id)
