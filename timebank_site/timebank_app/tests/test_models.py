from django.test import TestCase

from timebank_app.models import (
    User,
    Task,
    Interval,
)

# class UserModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         User.objects.create()

# class IntervalModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Set up non-modified objects used by all test methods
#         Task.objects.create()


class TaskModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def setUp(self):
        # Set up non-modified objects used by all test methods
        self.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        self.login = self.client.login(
            username='testuser',
            password='12345'
        )

        self.task = Task.objects.create(
            task_name='TEST',
            time_budget=3600,
            author=self.user
        )

# Check field labels
    def test_task_name_label(self):
        field_label = self.task._meta.get_field('task_name').verbose_name
        self.assertEquals(field_label, 'task name')
    def test_task_notes_label(self):
        field_label = self.task._meta.get_field('task_notes').verbose_name
        self.assertEquals(field_label, 'task notes')
    def test_parent_task_label(self):
        field_label = self.task._meta.get_field('parent_task').verbose_name
        self.assertEquals(field_label, 'parent task')
    def test_task_type_label(self):
        field_label = self.task._meta.get_field('task_type').verbose_name
        self.assertEquals(field_label, 'task type')
    def test_tasklist_label(self):
        field_label = self.task._meta.get_field('tasklist').verbose_name
        self.assertEquals(field_label, 'tasklist')
    def test_time_budget_label(self):
        field_label = self.task._meta.get_field('time_budget').verbose_name
        self.assertEquals(field_label, 'time budget')
    def test_complete_label(self):
        field_label = self.task._meta.get_field('complete').verbose_name
        self.assertEquals(field_label, 'complete')
    def test_running_label(self):
        field_label = self.task._meta.get_field('running').verbose_name
        self.assertEquals(field_label, 'running')
    def test_created_label(self):
        field_label = self.task._meta.get_field('created').verbose_name
        self.assertEquals(field_label, 'created')
    def test_last_added_label(self):
        field_label = self.task._meta.get_field('last_added').verbose_name
        self.assertEquals(field_label, 'last added')
    def test_last_modified_label(self):
        field_label = self.task._meta.get_field('last_modified').verbose_name
        self.assertEquals(field_label, 'last modified')
    def test_author_label(self):
        field_label = self.task._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

# Check string representation
    def test__str__method(self):
        string_rep = self.task.__str__()
        self.assertEquals(string_rep, '1: TEST')
