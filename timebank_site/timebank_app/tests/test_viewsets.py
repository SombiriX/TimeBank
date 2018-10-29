from django.db.models import F, Max
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIRequestFactory, APITestCase

from timebank_app.models import (
    User,
    Task,
    Interval,
)

from timebank_app.serializers import (
    UserSerializer,
    TaskSerializer,
    IntervalSerializer,
)

class TaskViewSetTest(APITestCase):
    # pylint: disable=too-many-instance-attributes
    # instances are necessary for testing
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser1',
            password='12345'
        )

        cls.other_user = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        cls.factory = APIRequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser1',
            password='12345'
        )

        self.task1 = Task.objects.create(
            task_name='TEST1',
            time_budget=30,
            author=self.user
        )

        self.other_user_task = Task.objects.create(
            task_name='TEST5',
            time_budget=86400,
            author=self.other_user
        )

        self.valid_payload1 = {
            'task_name': 'valid task',
            'time_budget': 4,
        }

        self.valid_payload2 = {
            'task_name': 'valid task',
        }

        self.invalid_payload1 = {
            'task_name': '',
            'time_budget': 4,
        }

        self.invalid_payload2 = {
        }

        self.invalid_payload3 = {
            'time_budget': 4,
        }

        self.invalid_payload4 = {
            'time_budget': '',
        }

    def test_get_all_tasks(self):
        test_url = reverse('task-list')
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        tasks = Task.objects.all()
        serializer = TaskSerializer(
            tasks,
            context={'request': request},
            many=True
        )

        response_set = set(t['id'] for t in response.data)
        all_tasks = set(t['id'] for t in serializer.data)

        # Check that the returned task list only contains tasks which
        # belong to the user who requested them
        set_diff = all_tasks.difference(response_set)

        self.assertEqual(len(set_diff), 1)
        self.assertEqual(set_diff.pop(), self.other_user_task.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task(self):
        test_pk = self.task1.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        task = Task.objects.get(pk=test_pk)
        serializer = TaskSerializer(
            task,
            context={'request': request}
        )

        self.assertEqual(
            response.data,
            serializer.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task_invalid(self):
        # Attempt to get nonexistent task
        max_id = Task.objects.all()\
            .aggregate(max_id=Max(F('id')))\
            .get('max_id', None)
        test_pk = max_id + 1
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_user_task(self):
        # Try to access another user's task
        test_pk = self.other_user_task.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_tasks_unauthenticated(self):
        # Try task listing while unauthenticated
        self.client.logout()
        test_url = reverse('task-list')
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_task_unauthenticated(self):
        # Try task listing while unauthenticated
        test_pk = self.task1.pk
        self.client.logout()
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task(self):
        test_url = reverse('task-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            test_url,
            data=self.valid_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_task_unauthenticated(self):
        self.client.logout()
        test_url = reverse('task-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task_invalid(self):
        test_url = reverse('task-list')

        response = self.client.post(
            test_url,
            data=self.invalid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            test_url,
            data=self.invalid_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            test_url,
            data=self.invalid_payload3
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.post(
            test_url,
            data=self.invalid_payload4
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_task(self):
        test_pk = self.task1.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        for (k, v) in self.valid_payload1.items():
            self.assertEqual(v, response.data[k])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_task(self):
        test_pk = self.other_user_task.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_task_unauthenticated(self):
        self.client.logout()
        test_pk = self.task1.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_task_invalid(self):
        test_pk = self.task1.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.invalid_payload1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_task(self):
        test_pk = self.task1.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.delete(
            test_url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(test_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(response.data.get('deleted', None))


class IntervalViewSetTest(APITestCase):
    # pylint: disable=too-many-instance-attributes
    # instances are necessary for testing
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser1',
            password='12345'
        )

        cls.other_user = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        cls.factory = APIRequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser1',
            password='12345'
        )

        self.task = Task.objects.create(
            task_name='TEST',
            time_budget=3600,
            author=self.user
        )

        self.other_user_task = Task.objects.create(
            task_name='TEST',
            time_budget=3600,
            author=self.other_user
        )

        self.interval1 = Interval.objects.create(
            author=self.user,
            task=self.task,
        )

        self.other_user_interval = Interval.objects.create(
            author=self.other_user,
            task=self.other_user_task,
        )

        self.valid_payload1 = {
            'task': self.task.id,
            'start': timezone.now() - timezone.timedelta(hours=1),
        }

        self.valid_payload2 = {
            'task': self.task.id,
            'start': timezone.now() - timezone.timedelta(minutes=15),
        }

        self.invalid_payload1 = {
            'start': timezone.now(),
        }

        self.invalid_payload2 = {
        }

        self.invalid_payload3 = {
            'task': self.task.id,
            'start': '',
        }

        self.invalid_payload4 = {
            'task': self.task.id,
            'stop': '',
        }

        self.invalid_payload5 = {
            'task': self.task.id,
            'start': timezone.now() - timezone.timedelta(minutes=10),
            'stop': timezone.now() - timezone.timedelta(minutes=20),
        }

        self.invalid_payload6 = {
            'task': self.task.id,
            'start': timezone.now() + timezone.timedelta(minutes=10),
            'stop': timezone.now() + timezone.timedelta(minutes=20),
        }

    def test_get_all_intervals(self):
        test_url = reverse('interval-list')
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        intervals = Interval.objects.all()
        serializer = IntervalSerializer(
            intervals,
            context={'request': request},
            many=True
        )

        response_set = set(t['id'] for t in response.data)
        all_intervals = set(t['id'] for t in serializer.data)

        # Check that the returned interval list only contains intervals which
        # belong to the user who requested them
        set_diff = all_intervals.difference(response_set)

        self.assertEqual(len(set_diff), 1)
        self.assertEqual(set_diff.pop(), self.other_user_interval.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_interval(self):
        test_pk = self.interval1.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        interval = Interval.objects.get(pk=test_pk)
        serializer = IntervalSerializer(
            interval,
            context={'request': request}
        )

        self.assertEqual(
            response.data,
            serializer.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_interval_invalid(self):
        # Attempt to get nonexistent interval
        max_id = Interval.objects.all()\
            .aggregate(max_id=Max(F('id')))\
            .get('max_id', None)
        test_pk = max_id + 1
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_user_interval(self):
        # Try to access another user's interval
        test_pk = self.other_user_interval.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_intervals_unauthenticated(self):
        # Try interval listing while unauthenticated
        self.client.logout()
        test_url = reverse('interval-list')
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_interval_unauthenticated(self):
        # Try interval listing while unauthenticated
        test_pk = self.interval1.pk
        self.client.logout()
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_interval(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            test_url,
            data=self.valid_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_interval_unauthenticated(self):
        self.client.logout()
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_interval_invalid(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_interval_invalid2(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_interval_invalid3(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload3
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_interval_invalid4(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload4
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_interval_invalid5(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload5
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_interval_invalid6(self):
        test_url = reverse('interval-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload6
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_interval(self):
        test_pk = self.interval1.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user_interval(self):
        test_pk = self.other_user_interval.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_interval_unauthenticated(self):
        self.client.logout()
        test_pk = self.interval1.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_interval_invalid(self):
        test_pk = self.interval1.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.invalid_payload1
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_interval(self):
        test_pk = self.interval1.pk
        test_url = reverse('interval-detail', kwargs={'pk': test_pk})

        response = self.client.delete(
            test_url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        test_pk = self.task.pk
        task_url = reverse('task-detail', kwargs={'pk': test_pk})

        response = self.client.delete(
            task_url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(
            test_url
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class UserViewSetTest(APITestCase):
    # pylint: disable=too-many-instance-attributes
    # instances are necessary for testing
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

        self.valid_payload1 = {
            'username': 'testuser1000',
            'password': '12345',
        }

        self.invalid_payload1 = {
            'username': '',
            'password': '12345',
        }

        self.invalid_payload2 = {
            'username': 'Testuser1000',
            'password': '',
        }

        self.questionable_payload1 = {
            'username': 'testuser1000',
            'password': '12345',
            'is_staff': True,
        }

        self.questionable_payload2 = {
            'username': 'testuser1000',
            'password': '12345',
            'is_active': True
        }

        self.questionable_payload3 = {
            'username': 'testuser1000',
            'password': '12345',
            'date_joined': timezone.now() + timezone.timedelta(days=1),
        }

    def test_get_all_users(self):
        test_url = reverse('user-list')
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(
            users,
            context={'request': request},
            many=True
        )

        response_set = set(t['id'] for t in response.data)
        all_users = set(t['id'] for t in serializer.data)

        # Check that the returned user list only contains the current user
        # and not any other users in the database
        set_diff = all_users.difference(response_set)

        self.assertEqual(len(set_diff), len(users) - 1)
        self.assertEqual(
            set_diff.difference({self.other_user1.id, self.other_user2.id}),
            set()
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_users_as_superuser(self):
        test_url = reverse('user-list')
        self.client.logout()
        self.client.login(
            username='superuser1',
            password='12345'
        )
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        users = User.objects.all()
        serializer = UserSerializer(
            users,
            context={'request': request},
            many=True
        )

        response_set = set(t['id'] for t in response.data)
        all_users = set(t['id'] for t in serializer.data)

        # Check that the returned user list only contains the current user
        # and not any other users in the database
        set_diff = all_users.difference(response_set)

        self.assertEqual(len(set_diff), len(users) - 1)
        self.assertEqual(
            set_diff.difference({self.user.id, self.other_user1.id}),
            set()
            )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user(self):
        test_pk = self.user.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})
        request = self.factory.get(test_url)
        response = self.client.get(test_url)
        # get data from db
        user = User.objects.get(pk=test_pk)
        serializer = UserSerializer(
            user,
            context={'request': request}
        )

        self.assertEqual(
            response.data,
            serializer.data
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_user_invalid(self):
        # Attempt to get nonexistent user
        max_id = User.objects.all()\
            .aggregate(max_id=Max(F('id')))\
            .get('max_id', None)
        test_pk = max_id + 1
        test_url = reverse('user-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_user(self):
        # Try to access another user's user
        test_pk = self.other_user1.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_users_unauthenticated(self):
        # Try user listing while unauthenticated
        self.client.logout()
        test_url = reverse('user-list')
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_one_user_unauthenticated(self):
        # Try user listing while unauthenticated
        test_pk = self.user.pk
        self.client.logout()
        test_url = reverse('user-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_invalid1(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_invalid2(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.invalid_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_unauthenticated(self):
        self.client.logout()
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_questionable1(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.questionable_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_questionable2(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.questionable_payload2
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_user_questionable3(self):
        test_url = reverse('user-list')
        response = self.client.post(
            test_url,
            data=self.questionable_payload3
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user(self):
        test_pk = self.user.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_other_user(self):
        test_pk = self.other_user1.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_user_unauthenticated(self):
        self.client.logout()
        test_pk = self.user.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.valid_payload1
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_questionable1(self):
        test_pk = self.user.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})

        response = self.client.put(
            test_url,
            data=self.questionable_payload1
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        test_pk = self.user.pk
        test_url = reverse('user-detail', kwargs={'pk': test_pk})

        response = self.client.delete(
            test_url
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
