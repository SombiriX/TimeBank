import json
from django.db.models import F, Max
from django.urls import reverse
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

from timebank_app.viewsets import (
    IntervalViewSet,
    TaskViewSet,
    UserViewSet,
)


class TaskViewSetTest(APITestCase):
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

        self.task2 = Task.objects.create(
            task_name='TEST2',
            time_budget=60,
            author=self.user
        )

        self.task3 = Task.objects.create(
            task_name='TEST3',
            time_budget=600,
            author=self.user
        )

        self.task4 = Task.objects.create(
            task_name='TEST4',
            time_budget=3600,
            author=self.user
        )

        self.other_user_task = Task.objects.create(
            task_name='TEST5',
            time_budget=86400,
            author=self.other_user
        )

    def test_get_all_tasks(self):
        # get API response
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

        self.assertEqual(
            set(json.dumps(response.data)),
            set(json.dumps(serializer.data))
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_task(self):
        # get API response
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
        # get API response
        max_id = Task.objects.all()\
            .aggregate(max_id=Max(F('id')))\
            .get('max_id', None)
        test_pk = max_id + 1
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_other_user_task(self):
        # get API response
        test_pk = self.other_user_task.pk
        test_url = reverse('task-detail', kwargs={'pk': test_pk})
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_all_tasks_unauthenticated(self):
        # get API response
        self.client.logout()
        test_url = reverse('task-list')
        response = self.client.get(test_url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task(self):
        # TODO
        pass

    def test_update_task(self):
        # TODO
        pass

    def test_delete_task(self):
        # TODO
        pass
