from django.db.models import F
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from timebank_app.models import User
from timebank_app.serializers import UserSerializer


class CurrentUserViewTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser1',
            password='12345'
        )

        cls.other_user1 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        cls.other_user2 = User.objects.create_superuser(
            username='superuser1',
            password='12345',
            email='super@example.com'
        )

        cls.factory = APIRequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser1',
            password='12345'
        )

    def test_get_user(self):
        test_pk = self.user.pk
        test_url = reverse('currentUser')
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(
            users,
            context={'request': request},
            many=True
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsInstance(response.data, dict)

        field_names = [
            'date_joined',
            'email',
            'first_name',
            'id',
            'last_login',
            'last_name',
            'user_prefs',
            'username',
        ]
        self.assertCountEqual(response.data.keys(), field_names)

        user_pref_field_names = [
            'complete_anim',
            'twentyFourClock',
        ]
        self.assertCountEqual(
            response.data['user_prefs'].keys(),
            user_pref_field_names
        )

        self.assertEqual(response.data['id'], test_pk)
