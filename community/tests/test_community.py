import pytest
from django.urls import reverse
from community.models import Post, Comment
from stockAnalysis.models import AnalyzedStock
from users.models import Profile
from django.utils import timezone
from django.contrib.auth.models import User


@pytest.fixture
def create_user_and_analyzed_stock():
    user = User.objects.create_user(username='testuser', password='testpassword')
    profile = Profile.objects.create(user_id=user)
    analyzed_stock = AnalyzedStock.objects.create(
        analyst_id=profile,
        stock_image={},
        description='Test stock',
        is_public=True
    )

    return user, analyzed_stock


@pytest.fixture
def post(create_user_and_analyzed_stock):
    user, analyzed_stock = create_user_and_analyzed_stock
    # Create and return the Post object as a fixture
    post = Post.objects.create(
        analysis_id=analyzed_stock,
        title='Test Post',
        description='Test Content'
    )
    return post


@pytest.fixture
def comment_form_data():
    return {'content': 'Test Comment Content'}


@pytest.mark.django_db
class TestSharePost:
    def test_create_post_view(self, client, create_user_and_analyzed_stock):
        user, analyzed_stock = create_user_and_analyzed_stock
        client.login(username='testuser', password='testpassword')
        url = reverse('create_post', kwargs={'pk': analyzed_stock.id})
        response = client.post(url, data={
            'title': 'Test Post',
            'description': 'This is a test post',
        })

        assert response.status_code == 200

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


@pytest.mark.django_db
class TestPostDeatils:
    def test_post_details_view(self, client, post):  # Use the post fixture here
        url = reverse('post_details', args=[post.id])
        response = client.get(url)

        assert response.status_code == 200

    def test_comment_view(self, client, create_user_and_analyzed_stock, post, comment_form_data):
        user, _ = create_user_and_analyzed_stock  # Unpack the tuple and get the user object
        client.login(username='testuser', password='testpassword')

        url = reverse('comment', args=[post.id])
        response = client.post(url, data=comment_form_data)

        assert response.status_code == 200

        assert Comment.objects.filter(publisher_id=user.profile, content=comment_form_data['content'],
                                      post_id=post).exists()
