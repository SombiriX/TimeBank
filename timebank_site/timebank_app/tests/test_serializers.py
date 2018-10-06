from django.test import RequestFactory, TestCase
from django.utils import timezone
from rest_framework.relations import Hyperlink

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


class UserSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        cls.factory = RequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser',
            password='12345'
        )

        self.test_user = User.objects.all()[0]
        self.request = self.factory.get('/some_path')
        self.serializer = UserSerializer(
            instance=self.test_user,
            context={'request': self.request})

    def test_field_names(self):
        # Check that serializer fields match expected values
        data = self.serializer.data

        field_names = [
            'username',
            'id',
            'first_name',
            'last_name',
            'tasks',
        ]
        self.assertCountEqual(data.keys(), field_names)


class IntervalSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        cls.factory = RequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser',
            password='12345'
        )

        self.task = Task.objects.create(
            task_name='TEST',
            time_budget=3600,
            author=self.user
        )

        self.interval_attributes = {
            'start': '2018-09-18T06:14:37.712159Z',
            'stop': '2018-09-18T07:14:37.712159Z',
            'task': self.task,
            'created': '',
            'last_modified': '',
        }

        self.interval = Interval.objects.create(
            **self.interval_attributes,
            author=self.user
        )
        self.request = self.factory.get('/some_path')
        self.serializer = IntervalSerializer(
            instance=self.interval,
            context={'request': self.request})

    def test_field_names(self):
        # Check that serializer fields match expected values
        data = self.serializer.data

        field_names = [
            'author',
            'created',
            'id',
            'last_modified',
            'start',
            'stop',
            'task',
        ]
        self.assertCountEqual(data.keys(), field_names)

    def test_author_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['author']),
            Hyperlink
        )

    def test_start_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['start'],
            self.interval_attributes['start']
        )

    def test_stop_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['stop'],
            self.interval_attributes['stop']
        )

    def test_created_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['created']),
            str
        )
    def test_last_modified_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['last_modified']),
            str
        )
    def test_task_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['task'],
            self.interval_attributes['task'].id
        )


class TaskSerializerTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        cls.factory = RequestFactory()

    def setUp(self):
        self.login = self.client.login(
            username='testuser',
            password='12345'
        )

        self.task_attributes = {
            'author': self.user,
            'complete': False,
            'last_added': None,
            'parent_task': None,
            'running': False,
            'task_name': 'TEST',
            'task_notes': 'BlahBlahBlahBlah',
            'task_type': 'D',
            'time_budget': 3600,
        }

        self.task = Task.objects.create(**self.task_attributes)
        self.request = self.factory.get('/some_path')
        self.serializer = TaskSerializer(
            instance=self.task,
            context={'request': self.request})

    def test_field_names(self):
        # Check that serializer fields match expected values
        data = self.serializer.data

        field_names = [
            'author',
            'complete',
            'created',
            'id',
            'intervals',
            'last_added',
            'last_modified',
            'parent_task',
            'running',
            'running_interval',
            'runtime',
            'task_name',
            'task_notes',
            'task_type',
            'tasklist',
            'time_budget',
        ]
        self.assertCountEqual(data.keys(), field_names)

    def test_author_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['author']),
            Hyperlink
        )

    def test_complete_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['complete'],
            self.task_attributes['complete']
        )

    def test_created_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['created']),
            str
        )

    def test_last_added_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['last_added'],
            self.task_attributes['last_added']
        )

    def test_last_modified_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            type(data['last_modified']),
            str
        )

    def test_parent_task_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['parent_task'],
            self.task_attributes['parent_task']
        )

    def test_running_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['running'],
            self.task_attributes['running']
        )

    def test_task_name_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['task_name'],
            self.task_attributes['task_name']
        )

    def test_task_notes_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['task_notes'],
            self.task_attributes['task_notes']
        )

    def test_task_type_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['task_type'],
            self.task_attributes['task_type']
        )

    def test_time_budget_field_content(self):
        data = self.serializer.data
        self.assertEqual(
            data['time_budget'],
            self.task_attributes['time_budget']
        )

    def test_task_running(self):
        running_task = Task.objects.create(**self.task_attributes)

        data1 = TaskSerializer(
            instance=running_task,
            context={'request': self.request}
        ).data

        right_now = timezone.now()
        an_hour_ago = right_now - timezone.timedelta(hours=1)
        thirty_mins_ago = right_now - timezone.timedelta(minutes=30)
        fifteen_mins_ago = right_now - timezone.timedelta(minutes=15)

        interval1 = Interval.objects.create(
            author=self.user,
            task=running_task,
            start=an_hour_ago,
            stop=thirty_mins_ago
        )
        interval2 = Interval.objects.create(
            author=self.user,
            task=running_task,
            start=fifteen_mins_ago
        )

        running_task.running = True
        running_task.save()

        data2 = TaskSerializer(
            instance=running_task,
            context={'request': self.request}
        ).data

        # Assert that time delta is within 1 second of 45 minutes
        self.assertAlmostEqual(
            data2['runtime'] - data1['runtime'],
            2700,
            delta=1
        )

        # Verify the running interval
        i1 = IntervalSerializer(
            instance=interval1, context={'request': self.request}
        )
        i2 = IntervalSerializer(
            instance=interval2, context={'request': self.request}
        )
        self.assertEqual(
            data2['running_interval'],
            i2.data
        )
        self.assertNotEqual(
            data1['running_interval'],
            i1.data
        )

        # Stop the running task and verify that running_interval is None
        interval2.stop = right_now
        interval2.save()

        running_task.running = False
        running_task.save()

        data3 = TaskSerializer(
            instance=running_task,
            context={'request': self.request}
        ).data

        self.assertIsNone(data3['running_interval'])
