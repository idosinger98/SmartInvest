import pytest
from django.utils import timezone
from community.models import Post
from community.models import Comment
from users.models import Profile
from stockAnalysis.models import AnalyzedStocks
from stockAnalysis.tests.testQueriesModel import test_user, test_analyzed_stock


@pytest.fixture
@pytest.mark.django_db
def make_post(db, test_analyzed_stock):
    def make(
        analysis_id: AnalyzedStocks = test_analyzed_stock,
        likes: int = 0,
        time: timezone = timezone.now(),
    ):
        post = Post.objects.create(analysis_id=analysis_id, likes=likes, time=time)
        return post

    return make


@pytest.fixture
@pytest.mark.django_db
def make_comment(db, make_post):
    def make(
        publisher_id: Profile = test_user,
        content: str = 'test comment',
        post_id: Post = make_post,
        likes: int = 0,
        time: timezone = timezone.now(),
    ):
        comment = Comment.objects.create(publisher_id=publisher_id,
                                         content=content,
                                         post_id=post_id,
                                         likes=likes,
                                         time=time)
        return comment

    return make


@pytest.fixture
@pytest.mark.django_db
def test_analyzed_stock2(db, test_user):
    # Create a test AnalyzedStocks object for testing
    analyzed_stock = AnalyzedStocks.objects.create(
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
    analyzed_stock = AnalyzedStocks.objects.create(
        analyst_id=test_user,
        stock_image={'symbol': 'AAPL', 'price': 150.0},
        description='Test description',
        is_public=True
    )
    return analyzed_stock
