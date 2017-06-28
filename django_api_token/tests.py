from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from django_api_token.models import Token


class TestAPIAuth(TestCase):
    def test_token_generation_happy_path(self):
        user = User.objects.create_user(username='test_user', email='email@email.com', password='password')

        response = self.client.post(reverse('api:token'), {'username': 'test_user', 'password': 'password'})

        self.assertEqual(200, response.status_code)

        self.assertIn('token', response.json())
        self.assertIn('expires_at', response.json())

        expires_at = response.json()['expires_at']
        token = response.json()['token']

        token_model = Token.objects.get(user=user)

        self.assertEqual(token, token_model.token)
        self.assertEqual(expires_at, token_model.expires_at.isoformat())

    def test_token_generation_overwrites_old(self):
        pass

    def test_token_generation_with_wrong_credentials(self):
        pass