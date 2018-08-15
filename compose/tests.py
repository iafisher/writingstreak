from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from . import views


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


TMP_USER = 'temporary'
TMP_PWD = 'pwd'


class TestPages(TestCase):
    """Test that the proper templates are used to render pages."""

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(TMP_USER, 'temporary@example.com', TMP_PWD)

    def test_index_page_template(self):
        self.client.login(username=TMP_USER, password=TMP_PWD)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'compose/index.html')

    def test_login_page_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'compose/login.html')


class TestRedirects(TestCase):
    def setUp(self):
        User = get_user_model()
        User.objects.create_user(TMP_USER, 'temporary@example.com', TMP_PWD)

    def test_login_page_redirects(self):
        self.client.login(username=TMP_USER, password=TMP_PWD)
        response = self.client.get('/login')
        self.assertRedirects(response, '/')

    def test_index_page_redirects(self):
        response = self.client.get('/')
        self.assertRedirects(response, '/login/?next=/')
