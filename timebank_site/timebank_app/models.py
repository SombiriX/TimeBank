from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.db.models import (
    BooleanField,
    CASCADE,
    CharField,
    DateTimeField,
    DurationField,
    ForeignKey,
    IntegerField,
    ManyToManyField,
    Model,
    TextField,
)
from django.utils import timezone


class User(AbstractUser):
    complete_anim = IntegerField(default=0)
    created = DateTimeField(auto_now_add=True)
    last_modified = DateTimeField(auto_now=True)


class Task(Model):
    discrete = 'D'
    recurring = 'C'
    TASK_TYPE_CHOICES = (
        (discrete, 'Discrete'),
        (recurring, 'Recurring'))

    task_name = CharField(
        max_length=115,
        default='',)
    task_notes = TextField(null=True)
    parent_task = ForeignKey(
        'self',
        on_delete=CASCADE,
        null=True,)
    task_type = CharField(
        max_length=1,
        choices=TASK_TYPE_CHOICES,
        default=discrete,)
    tasklist = ManyToManyField(
        'self',)
    time_budget = DurationField(default=timedelta(0))
    is_complete = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    last_added = DateTimeField(null=True)
    last_modified = DateTimeField(auto_now=True)
    author = ForeignKey(User, related_name='tasks', on_delete=CASCADE)


class Interval(Model):
    start = DateTimeField(default=timezone.now)
    stop = DateTimeField(null=True)
    task = ForeignKey(
        Task,
        related_name='intervals',
        on_delete=CASCADE,
        null=True
    )
    created = DateTimeField(auto_now_add=True)
    last_modified = DateTimeField(auto_now=True)
