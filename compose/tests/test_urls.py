from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve

from compose import views


TEST_USER = 'temporary'
TEST_PWD = 'pwd'


class TestURLs(TestCase):
    """Test that URLs resolve to the expected views."""

    def test_can_resolve_index(self):
        found = resolve('/')
        self.assertEqual(found.func, views.index)

    def test_can_resolve_login(self):
        found = resolve('/login')
        self.assertEqual(found.func, views.login)

    def test_can_resolve_logout(self):
        found = resolve('/logout')
        self.assertEqual(found.func, views.logout)

    def test_can_resolve_archive(self):
        found = resolve('/archive/2018/8/22')
        self.assertEqual(found.func, views.archive)


class TestRedirects(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(TEST_USER, 'temporary@example.com', TEST_PWD)

    def test_login_page_redirects(self):
        self.client.login(username=TEST_USER, password=TEST_PWD)
        response = self.client.get('/login')
        self.assertRedirects(response, '/')

    def test_index_page_redirects(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
