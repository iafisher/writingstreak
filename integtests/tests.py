"""Integration tests for the Writing Streak site.

Author:  Ian Fisher (iafisher@protonmail.com)
Version: August 2018
"""
import time

from django.contrib.auth import get_user_model
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from compose.models import DailyEntry


TEST_USER = 'testuser'
TEST_PWD = 'Temporary'


class NewVisitorTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        User = get_user_model()
        self.user = User.objects.create_user(TEST_USER, 'temporary@example.com',
            TEST_PWD)

    def tearDown(self):
        self.browser.quit()

    def test_can_make_entry(self):
        self.log_myself_in()

        text_input = self.browser.find_element_by_id('text-input')
        text_input.send_keys('Lorem ipsum')

        time.sleep(0.5)

        entry = DailyEntry.objects.today(user=self.user)
        self.assertEqual(entry.text, 'Lorem ipsum')

        paragraphs = self.browser.find_elements_by_tag_name('p')
        text = ' '.join(p.text for p in paragraphs)

        self.assertIn('2 words', text)
        self.assertIn('(2 to date, 2 this month)', text)
        self.assertIn('You need 98 more words to meet your daily goal of ' +
            '100 words.', text)
        self.assertIn('You are on a 0 day streak.', text)
        self.assertIn('Your longest streak was 1 day.', text)

    def log_myself_in(self):
        self.browser.get(self.live_server_url + '/login')
        username_input = self.browser.find_element_by_id('id_username')
        username_input.send_keys(TEST_USER)
        password_input = self.browser.find_element_by_id('id_password')
        password_input.send_keys(TEST_PWD)

        self.browser.find_element_by_id('submit').click()
        self.wait_for_index_page_load()

    def wait_for_index_page_load(self):
        start_time = time.time()
        while 'Login' in self.browser.title:
            if time.time() - start_time > MAX_WAIT:
                raise Exception('Timed out while trying to load the index page')
            time.sleep(0.1)
