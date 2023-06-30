import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from review.models import Review
from users.models import Profile


@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    client.force_login(user)
    Profile.objects.create(user_id=user, phone_number='1234567890', country='US')
    return client


@pytest.mark.django_db
class TestCreateReviewView:
    def test_create_review_valid(self, authenticated_user):
        response = authenticated_user.get(reverse('create_review'))
        assert response.status_code == 200

        response = authenticated_user.post(reverse('create_review'), {
         'content': 'This is a test review',
         'rating': 5
         })

        # Check that the response redirects to the desired page (change_password)
        assert response.status_code == 302
        assert response.url == reverse('change_password')

        # Check that a review is created in the database
        assert Review.objects.filter(publisher_id__user_id__username='testuser').count() == 1

    def test_create_review_invalid(self, authenticated_user):
        # Send a POST request to the create review view without providing a rating
        response = authenticated_user.post(reverse('create_review'), {
         'content': 'This is another test review',
         'rating': ''
        })

        # Check that the response status code is 200 (OK) and error message is displayed
        assert response.status_code == 200
        assert b"You must enter rating" in response.content
        assert Review.objects.filter(publisher_id__user_id__username='testuser').count() == 0

        # Send a POST request to the create review view when the user already has a review
        response = authenticated_user.post(reverse('create_review'), {
            'content': 'This is a test review',
            'rating': 5
        })

        response = authenticated_user.post(reverse('create_review'), {
            'content': 'New review',
            'rating': 3
        })

        # Check that the response status code is 200 (OK) and error message is displayed
        assert response.status_code == 200
        assert b"You have already given a review on the site" in response.content
        assert Review.objects.filter(publisher_id__user_id__username='testuser').count() == 1
