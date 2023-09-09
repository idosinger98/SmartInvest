import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from users.forms import LoginForm, RegisterForm, ProfileForm
from users.models import Profile

USERNAME = "testusername3"
PASSWORD = 'testpassword3'


@pytest.fixture
def authenticated_user(client):
    user = User.objects.create_user(username='testuser', password='testpassword')
    Profile.objects.create(user_id=user, phone_number='1234567890', country='US')
    client.force_login(user)
    return client


@pytest.fixture
def unauthenticated_user():
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    return Profile.objects.create(user_id=user, phone_number='1234567890', country='US')


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert 'users/login.html' in response.templates[0].name

    def test_sign_in_POST_valid(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        Profile.objects.create(user_id=user, phone_number='1234567890', country='US')
        response = client.post('/login/', {
            'username': "testuser",
            'password': "testpassword",
        })
        assert response.status_code == 302
        assert response.url == reverse('landing_page')

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
            'country': 'US',  # Add the country field with a valid value
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

    def test_sign_up_POST_invalid(self):
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


@pytest.mark.django_db
class TestChangePasswordView:
    def test_password_change_view(self, authenticated_user):
        url = reverse('change_password')
        response = authenticated_user.get(url)
        assert response.status_code == 200

    def test_password_change_POST(self, client):
        user = User.objects.create_user(username='testuser', password='testpassword')
        client.force_login(user)
        url = reverse('change_password')
        data = {
            'old_password': 'testpassword',
            'new_password1': 'newtestpassword',
            'new_password2': 'newtestpassword',
        }
        response = client.post(url, data)
        assert response.status_code == 302  # Check for a redirect
        assert response.url == reverse('show_details')  # Check the redirect URL
        user.refresh_from_db()
        assert user.check_password('newtestpassword')  # Verify the password change


@pytest.mark.django_db
class TestEditProfileView:
    def test_get_edit_profile_view(self, authenticated_user):
        response = authenticated_user.get(reverse('edit_profile'))
        assert response.status_code == 200
        assert 'users/edit_profile.html' in response.templates[0].name
        assert 'user_form' in response.context
        assert 'profile_form' in response.context

    def test_post_valid_form(self, authenticated_user):
        data = {
            'username': 'newusername',
            'email': 'newemail@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'country': 'US',
        }
        response = authenticated_user.post(reverse('edit_profile'), data=data)
        assert response.status_code == 302
        assert response.url == reverse('show_details')

        # Perform additional assertions to check the updated user and profile data
        user = User.objects.get(username='newusername')
        assert user.email == 'newemail@example.com'
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        profile = user.profile
        assert profile.phone_number == '1234567890'
        assert profile.country == 'US'

    def test_post_invalid_form(self, authenticated_user):
        # Simulate an invalid form submission
        data = {
            'username': '',  # Invalid, username is required
            'email': '',  # Invalid, email is required
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'country': 'US',
        }
        response = authenticated_user.post(reverse('edit_profile'), data=data)
        assert response.status_code == 200
        assert 'users/edit_profile.html' in response.templates[0].name


@pytest.mark.django_db
class TestResetPasswordView:
    def test_get_reset_password_page(self, client):
        response = client.get('/password-reset/')
        assert response.status_code == 200
        assert 'users/password_reset.html' in [t.name for t in response.templates]

    def test_post_reset_password_valid(self, client, unauthenticated_user):
        response = client.post('/password-reset/', {'email': 'test@example.com'})
        assert response.status_code == 200
        assert 'users/reset_password_done.html' in [t.name for t in response.templates]

    def test_post_reset_password_invalid(self, client, unauthenticated_user):
        response = client.post('/password-reset/', {'email': 'invalid_email'})
        assert response.status_code == 200
        assert 'users/password_reset.html' in [t.name for t in response.templates]
