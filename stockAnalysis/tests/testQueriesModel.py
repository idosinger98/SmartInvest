import pytest
from django.contrib.auth.models import User
from django.db.models import QuerySet
from users.models import Profile
from stockAnalysis.models import AnalyzedStocks


@pytest.fixture
@pytest.mark.django_db
def test_user(db):
    # Create a test user object for the analyst_id field
    user = User.objects.create_user(username='test_user', password='test_password')
    profile = Profile.objects.create(user_id=user, phone_number='1234567890')
    return profile


@pytest.fixture
@pytest.mark.django_db
def test_analyzed_stock(db, test_user):
    # Create a test AnalyzedStocks object for testing
    analyzed_stock = AnalyzedStocks.objects.create(
        analyst_id=test_user,
        stock_image={'symbol': 'AAPL', 'price': 150.0},
        description='Test description',
        is_public=True
    )
    return analyzed_stock


@pytest.mark.django_db
def test_get_user_stocks(test_user, test_analyzed_stock):
    # Test the get_user_stocks() method
    user_stocks = AnalyzedStocks.objects.get_user_stocks(test_user.id)
    assert isinstance(user_stocks, QuerySet)
    assert test_analyzed_stock in user_stocks


@pytest.mark.django_db
def test_get_community_stocks(test_analyzed_stock):
    # Test the get_community_stocks() method
    community_stocks = AnalyzedStocks.objects.get_community_stocks()
    assert isinstance(community_stocks, QuerySet)
    assert test_analyzed_stock in community_stocks
