import pytest


@pytest.fixture
def create_users_themes(user):
    from notes.models import Theme

    another_theme = Theme.objects.create(title='some_title')
    another_theme.author.add(user.id)
