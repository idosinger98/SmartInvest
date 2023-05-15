import pytest
from django.contrib.auth.models import User
from django.urls import reverse


USERNAME = "test1"
PASSWORD = 'PASSWORD'


@pytest.fixture
def new_user():
    user = User(username=USERNAME,
                first_name="test",
                last_name="mctest",
                email="test123@gmail.com")

    user.set_password(PASSWORD)
    return user


@pytest.fixture
def persist_user(new_user):
    new_user.save()
    return new_user


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200

    def test_sign_in_POST_valid(self, client, persist_user):
        response = client.post('/login/', {
            'username': USERNAME,
            'password': PASSWORD,
        })
        assert response.status_code == 302
        assert response.url == reverse('login')

    def test_sign_in_POST_invalid(self, client):
        response = client.post('/login/', {
            'username': "test2",
            'password': PASSWORD,
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.content


@pytest.mark.django_db
class TestLogoutView:
    def test_sign_out(self, client, persist_user):
        client.force_login(user=persist_user)
        response = client.get('/logout/')
        assert response.status_code == 302
        assert response.url == reverse('login')


@pytest.mark.django_db
class TestResetPasswordView:
    def test_enter_reset_password_page(self, client):
        response = client.get('/password-reset/')
        assert response.status_code == 200

    def test_reset_password_POST_valid(self, client, persist_user):
        response = client.post('/password-reset/', {
            'email': 'test123@gmail.com',
        })
        assert response.status_code == 200
        assert b'Password reset email has been sent' in response.content

    def test_reset_password_POST_invalid(self, client):
        response = client.post('/password-reset/', {
            'email': 'invalid@gmail.com',
        })
        assert response.status_code == 200
        assert b'The email is not found in the system' in response.content
