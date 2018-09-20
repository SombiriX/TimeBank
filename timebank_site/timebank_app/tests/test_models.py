from django.db import DataError, transaction
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
        # Set up non-modified objects used by all test methods
        cls.user = User.objects.create_user(
            username='testuser',
            password='12345'
        )

        cls.name_limit = 115
        cls.valid_name_lt = ''.join('a' for x in range(cls.name_limit-1))
        cls.valid_name_eq = ''.join('a' for x in range(cls.name_limit))
        cls.invalid_name = ''.join('a' for x in range(cls.name_limit+1))

        cls.valid_types = ['C', 'D']
        cls.invalid_types = ['A', 'aa', '']

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

# Check field labels
    def test_task_name_label(self):
        field_label = self.task._meta.get_field('task_name').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'task name')
    def test_task_notes_label(self):
        field_label = self.task._meta.get_field('task_notes').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'task notes')
    def test_parent_task_label(self):
        field_label = self.task._meta.get_field('parent_task').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'parent task')
    def test_task_type_label(self):
        field_label = self.task._meta.get_field('task_type').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'task type')
    def test_tasklist_label(self):
        field_label = self.task._meta.get_field('tasklist').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'tasklist')
    def test_time_budget_label(self):
        field_label = self.task._meta.get_field('time_budget').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'time budget')
    def test_complete_label(self):
        field_label = self.task._meta.get_field('complete').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'complete')
    def test_running_label(self):
        field_label = self.task._meta.get_field('running').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'running')
    def test_created_label(self):
        field_label = self.task._meta.get_field('created').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'created')
    def test_last_added_label(self):
        field_label = self.task._meta.get_field('last_added').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'last added')
    def test_last_modified_label(self):
        field_label = self.task._meta.get_field('last_modified').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'last modified')
    def test_author_label(self):
        field_label = self.task._meta.get_field('author').verbose_name #pylint: disable=W0212
        self.assertEqual(field_label, 'author')

# Check string representation
    def test__str__method(self):
        string_rep = self.task.__str__()
        self.assertEqual(string_rep, '1: TEST')

# Check character limits
    def test_task_name_length_lt(self):
        self.task.task_name = self.valid_name_lt
        try:
            self.task.save()
        except DataError:
            self.fail("Raised DataError unexpectedly!")
    def test_task_name_length_eq(self):
        self.task.task_name = self.valid_name_eq
        try:
            self.task.save()
        except DataError:
            self.fail("Raised DataError unexpectedly!")
    def test_task_name_length_gt(self):
        self.task.task_name = self.invalid_name
        try:
            self.task.save()
        except DataError:
            self.assertTrue(True)
            return
        self.fail("Expected to raise DataError")
    def test_task_type_valid(self):
        try:
            for t in self.valid_types:
                self.task.task_type = t
                self.task.save()
        except DataError:
            self.fail("Raised DataError unexpectedly!")
    def test_task_type_invalid(self):
        exceptions = 0
        for t in self.invalid_types:
            try:
                with transaction.atomic():
                    self.task.task_type = t
                    self.task.save()
            except DataError:
                exceptions += 1
                continue
        self.assertEqual(
            exceptions,
            1,
            "Did not fail for correct number of cases"
        )
