from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework.test import APIRequestFactory

from polls import apiviews
# Create your tests here.
class TestPoll(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.view = apiviews.PollViewSet.as_view({'get': 'list'})
        self.uri = '/polls/'
        self.user = self.setup_user()

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            username = 'test',
            email = 'test@test.com',
            password = 'test'
        )

    def test_list(self):
        request = self.factory.get(self.uri)
        request.user = self.user
        response = self.view(request)      
        self.assertEqual(response.status_code, 200, \
        'Expected Response Code 200, received {0} instead'.format(response.status_code))

    def test_list2(self):
        self.client.login(username='test', password='test')
        response = self.client.get(self.uri)
        self.assertEqual(response.status_code, 200, \
        'Expected Response Code 200, received {0} instead'.format(response.status_code))

    def test_create(self):
        self.client.login(username='test', password='test')
        params = {
            "question": "Test",
            "created_by": 1
        }
        response = self.client.post(self.uri, params)
        self.assertEqual(response.status_code, 201, \
        'Expected Response Code 200, received {0} instead'.format(response.status_code))