import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from compose import models


TEST_USER = 'temporary'
TEST_PWD = 'pwd'


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
