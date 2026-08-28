from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class LoginTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_login(self):
        response = self.client.post(
            reverse("login"),
            {
                "username": "testuser",
                "password": "testpassword",
            }
        )

        self.assertRedirects(
            response,
            reverse("home")
        )

    def test_home_requires_login(self):
        response = self.client.get(
            reverse("home")
        )

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('home')}"
        )

    def test_home_after_login(self):
        self.client.login(
            username="testuser",
            password="testpassword"
        )

        response = self.client.get(
            reverse("home")
        )

        self.assertEqual(
            response.status_code,
            200
        )