from datetime import timedelta
from django.contrib.auth.models import AbstractUser
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
    twentyFourClock = BooleanField(default=False)
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
        default='',
    )
    task_notes = TextField(blank=True)
    parent_task = ForeignKey(
        'self',
        on_delete=CASCADE,
        blank=True,
        null=True,
    )
    task_type = CharField(
        max_length=1,
        choices=TASK_TYPE_CHOICES,
        default=discrete,)
    tasklist = ManyToManyField(
        'self',
        blank=True,
    )
    time_budget = DurationField(default=timedelta(0))
    complete = BooleanField(default=False)
    running = BooleanField(default=False)
    created = DateTimeField(auto_now_add=True)
    last_added = DateTimeField(blank=True, null=True)
    last_modified = DateTimeField(auto_now=True)
    author = ForeignKey(User, related_name='tasks', on_delete=CASCADE)

    def __str__(self):
        return "{}: {}".format(self.pk, self.task_name)


class Interval(Model):
    start = DateTimeField(default=timezone.now)
    stop = DateTimeField(blank=True, null=True)
    task = ForeignKey(
        Task,
        related_name='intervals',
        on_delete=CASCADE,
    )
    created = DateTimeField(auto_now_add=True)
    last_modified = DateTimeField(auto_now=True)

    def __str__(self):
        return "{}: {} - {}".format(self.pk, self.start, self.stop)
