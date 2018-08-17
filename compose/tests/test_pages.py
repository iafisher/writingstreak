from django.contrib.auth import get_user_model
from django.test import TestCase


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
