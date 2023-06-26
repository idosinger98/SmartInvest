import pytest
from users.forms import LoginForm, RegisterForm, ProfileForm
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Profile

USERNAME = "testusername3"
PASSWORD = 'testpassword3'


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert 'users/login.html' in response.templates[0].name

    def test_sign_in_POST_invalid(self, client):
        response = client.post('/login/', {
            'username': "test2",
            'password': PASSWORD,
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.content

    def test_login_form_validity(self):
        data = {
            'username': USERNAME,
            'password': PASSWORD,
        }

        form = LoginForm(data)
        assert form.is_valid()


@pytest.mark.django_db
class TestSignUpView:
    def test_enter_register_page(self, client):
        response = client.get(reverse('register'))
        assert response.status_code == 200
        assert 'users/register.html' in response.templates[0].name

    def test_sign_up_POST_valid(self, client):
        # Create a test user data
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }

        # Create a test profile data
        profile_data = {
            'phone_number': '1234567890',
        }

        user_form = RegisterForm(user_data)
        profile_form = ProfileForm(profile_data)
        assert user_form.is_valid()
        assert profile_form.is_valid()

        # Submit the sign-up form
        response = client.post(reverse('register'), data={**user_data, **profile_data}, follow=True)

        # Check the response status code and redirect
        assert response.status_code == 200
        assert response.redirect_chain[0][1] == 302  # Check the redirect status code
        assert response.redirect_chain[0][0] == reverse('login')  # Check the redirect URL

        # Check that the user and profile were created
        assert User.objects.filter(username='testuser').exists()
        assert Profile.objects.filter(user_id__username='testuser').exists()

    def test_sign_up_POST_invalid(self, client):
        user_data = {
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword11',
        }

        user_form = RegisterForm(user_data)
        assert not user_form.is_valid()
        assert not User.objects.filter(username='testuser').exists()
