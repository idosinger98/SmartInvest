import pytest
from django.contrib.messages import get_messages
from django.urls import reverse


@pytest.mark.django_db
class TestContactView:
    def test_contact_form_get_request(self, client):
        url = reverse('contact')
        response = client.get(url)
        assert response.status_code == 400

    def test_contact_form_post_invalid_email(self, client):
        url = reverse('contact')
        form_data = {
            'name': 'John Doe',
            'email': 'invalid_email',
            'subject': 'Test Subject',
            'message': 'Test Message',
        }
        response = client.post(url, data=form_data, follow=True)
        assert response.status_code == 400
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 0

    def test_contact_form_post_blank_data(self, client):
        url = reverse('contact')
        form_data = {}
        response = client.post(url, data=form_data, follow=True)
        assert response.status_code == 400
        messages = list(get_messages(response.wsgi_request))
        assert len(messages) == 0
