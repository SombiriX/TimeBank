from django.test import RequestFactory, TestCase
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

        self.serializer_data = {
            'task_name': 'TASK NAME',
            'time_budget': 600,
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
