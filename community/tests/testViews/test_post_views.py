import pytest
from django.urls import reverse
from community.models import Post


@pytest.mark.django_db
class TestPostView:
    def test_enter_community_page(self, client):
        response = client.get(reverse('community'))
        assert response.status_code == 200
        assert 'community/community.html' in response.templates[0].name
