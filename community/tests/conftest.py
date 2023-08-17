import pytest
from django.utils import timezone
from community.models import Post
from community.models import Comment
from django.contrib.auth.models import User
from users.models import Profile
from stockAnalysis.models import AnalyzedStock


@pytest.fixture
@pytest.mark.django_db
def test_user(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user', password='test_password')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890', country='US')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_user2(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user2', password='test_password2')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_user3(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user3', password='test_password3')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_user4(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user4', password='test_password4')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_user5(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user5', password='test_password5')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_analyzed_stock(db, test_user):
    # Create a test AnalyzedStocks object for testing
    analyzed_stock = AnalyzedStock.objects.create(
        analyst_id=test_user,
        stock_image={'symbol': 'AAPL', 'price': 150.0},
        description='Test description',
        is_public=True
    )
    return analyzed_stock


@pytest.fixture
@pytest.mark.django_db
def test_analyzed_stock2(db, test_user):
    # Create a test AnalyzedStocks object for testing
    analyzed_stock = AnalyzedStock.objects.create(
        analyst_id=test_user,
        stock_image={'symbol': 'AAPL', 'price': 150.0},
        description='Test description',
        is_public=True
    )
    return analyzed_stock


@pytest.fixture
@pytest.mark.django_db
def test_analyzed_stock3(db, test_user):
    # Create a test AnalyzedStocks object for testing
    analyzed_stock = AnalyzedStock.objects.create(
        analyst_id=test_user,
        stock_image={'symbol': 'AAPL', 'price': 150.0},
        description='Test description',
        is_public=True
    )
    return analyzed_stock


@pytest.fixture
@pytest.mark.django_db
def make_post(db, test_analyzed_stock):
    def make(
        analysis_id: AnalyzedStock = test_analyzed_stock,
        title: str = 'test title',
        likes: list = [],
        time: timezone = timezone.now(),
    ):
        post = Post.objects.create(analysis_id=analysis_id, title=title, time=time)
        for profile in likes:
            post.likes.add(profile)

        return post

    return make


@pytest.fixture
@pytest.mark.django_db
def make_comment(db, make_post, test_user):
    def make(
        publisher_id: Profile = test_user,
        content: str = 'test comment',
        post_id: Post = make_post,
        likes: list = [],
        time: timezone = timezone.now(),
    ):

        comment = Comment.objects.create(
            publisher_id=publisher_id,
            content=content,
            post_id=post_id,
            time=time
        )
        for profile in likes:
            comment.likes.add(profile)
        return comment

    return make
