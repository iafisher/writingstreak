import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve
from . import models, views


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


TEST_USER = 'temporary'
TEST_PWD = 'pwd'


class TestPages(TestCase):
    """Test that the proper templates are used to render pages."""

    def setUp(self):
        User = get_user_model()
        User.objects.create_user(TEST_USER, 'temporary@example.com', TEST_PWD)

    def test_index_page_template(self):
        self.client.login(username=TEST_USER, password=TEST_PWD)
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'compose/index.html')

    def test_login_page_template(self):
        response = self.client.get('/login')
        self.assertTemplateUsed(response, 'compose/login.html')


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


class TestModels(TestCase):
    def test_word_count_updated_on_save(self):
        User = get_user_model()
        u = User.objects.create_user(TEST_USER, 'temporary@example.com',
            TEST_PWD)
        entry = models.DailyEntry(date=datetime.date.today(),
            text='Lorem ipsum', user=u)

        entry.save()

        self.assertEqual(entry.word_count, 2)

    def test_calculate_word_count(self):
        entry = models.DailyEntry(text=' so--if  the minister-president is...')
        self.assertEqual(5, entry.calculate_word_count())

    def test_get_absolute_url(self):
        User = get_user_model()
        u = User.objects.create_user(TEST_USER, 'temporary@example.com',
            TEST_PWD)
        date = datetime.date(year=2018, month=8, day=1)
        entry = models.DailyEntry(date=date, text='Lorem ipsum', user=u)

        url = entry.get_absolute_url()

        self.assertEqual(url, '/archive/2018/8/1')
