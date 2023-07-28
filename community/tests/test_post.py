import pytest
from django.urls import reverse
from community.models import Post
from stockAnalysis.models import AnalyzedStocks
from users.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User


@pytest.fixture
def create_user_and_analyzed_stock():
    user = User.objects.create_user(username='testuser', password='testpassword')
    profile = Profile.objects.create(user_id=user)
    analyzed_stock = AnalyzedStocks.objects.create(analyst_id=profile, stock_image={}, description='Test stock',
                                                   is_public=True)
    return user, analyzed_stock


@pytest.mark.django_db
class TestCommunityApp:
    def test_create_post_view(self, client, create_user_and_analyzed_stock):
        user, analyzed_stock = create_user_and_analyzed_stock
        client.login(username='testuser', password='testpassword')
        url = reverse('create_post', kwargs={'pk': analyzed_stock.id})
        response = client.post(url, data={
            'title': 'Test Post',
            'description': 'This is a test post',
        })

        assert response.status_code == 200

    # Check if the post was created and saved to the database
        assert Post.objects.filter(analysis_id=analyzed_stock).exists()
        post = Post.objects.get(analysis_id=analyzed_stock)
        assert post.title == 'Test Post'
        assert post.description == 'This is a test post'
        assert post.likes == 0
        assert post.time <= timezone.now()

    def test_create_post_view_invalid_form(self, client, create_user_and_analyzed_stock):
        user, analyzed_stock = create_user_and_analyzed_stock
        client.login(username='testuser', password='testpassword')
        url = reverse('create_post', kwargs={'pk': analyzed_stock.id})
        response = client.post(url, data={})

        assert response.status_code == 200
        assert 'form' in response.context
        assert response.context['form'].errors

    def test_create_post_view_get(self, client, create_user_and_analyzed_stock):
        user, analyzed_stock = create_user_and_analyzed_stock
        client.login(username='testuser', password='testpassword')
        url = reverse('create_post', kwargs={'pk': analyzed_stock.id})
        response = client.get(url)

        assert response.status_code == 200
        assert 'form' in response.context
