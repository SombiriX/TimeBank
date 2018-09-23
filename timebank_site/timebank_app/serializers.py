from datetime import timedelta
from django.db.models import F, Sum
from django.utils import timezone
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError,
)
from .models import (
    Task,
    Interval,
    User,
)


class UserSerializer(ModelSerializer):

    tasks = HyperlinkedIdentityField(view_name='user-tasks')

    def validate(self, attrs):
        if self.initial_data.get('password', None) in ('', None):
            raise ValidationError("Blank passwords are not allowed")

        # Remove unsettable attribute values if provided
        if 'is_staff' in attrs.keys():
            del attrs['is_staff']
        if 'is_active' in attrs.keys():
            del attrs['is_active']
        if 'date_joined' in attrs.keys():
            del attrs['date_joined']

        return attrs

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'tasks',
        )


class TaskSerializer(ModelSerializer):
    author = HyperlinkedRelatedField(view_name='user-detail', read_only=True)
    intervals = HyperlinkedIdentityField(view_name='task-intervals')
    running_interval = SerializerMethodField()
    runtime = SerializerMethodField()

    def get_running_interval(self, instance):
        # Returns the most recent interval related to the task
        if instance.running:
            most_recent_interval = Interval.objects.filter(
                task__pk=instance.pk).order_by('-created')[0]
            return IntervalSerializer(most_recent_interval).data

        return None

    def get_runtime(self, instance):
        # Calculate how long the tasks has run for to the nearest second
        res = Interval.objects.filter(task__pk=instance.pk).order_by('-created')
        recorded_time = res\
            .annotate(task_duration=F('stop') - F('start'))\
            .aggregate(total_duration=Sum(F('task_duration')))\
            .get('total_duration', None)

        active_time = timedelta(0)
        if instance.running:
            # Get the most recent interval and calculate the runtime
            # at this moment
            running_interval = res[0]
            active_time = timezone.now() - running_interval.start

        ret = (active_time + recorded_time) if recorded_time else active_time

        return int(round(ret.total_seconds()))

    def get_validation_exclusions(self, *args, **kwargs):
        # exclude the author field since it's supplied in view later
        exclusions = super(
            TaskSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['author']

    def validate(self, attrs):
        # Verify that required fields are properly formatted
        t_name = attrs.get('task_name', None)
        t_budget = attrs.get('time_budget', None)

        if t_name in ('', None) or not isinstance(t_name, str):
            raise ValidationError('A valid task_name is required')
        if t_budget is not None and not isinstance(t_budget, int):
            raise ValidationError(
                'Time budget should be integer seconds'
            )

        # Remove unsettable attribute values if provided
        if 'running' in attrs.keys():
            del attrs['running']
        if 'author' in attrs.keys():
            del attrs['author']
        if 'intervals' in attrs.keys():
            del attrs['intervals']
        if 'running_interval' in attrs.keys():
            del attrs['running_interval']
        if 'runtime' in attrs.keys():
            del attrs['runtime']

        return attrs

    class Meta:
        model = Task
        fields = '__all__'


class IntervalSerializer(ModelSerializer):

    def validate(self, attrs):
        # Ensure stop time is after start time and
        # both start / stop times are in the past or present
        i_start = attrs.get('start', None)
        i_stop = attrs.get('stop', None)
        has_stop = i_stop is not None

        right_now = timezone.now()
        if not isinstance(i_start, timezone.datetime):
            raise ValidationError('Invalid start value')
        if has_stop and not isinstance(i_stop, timezone.datetime):
            raise ValidationError('Invalid stop value')
        if has_stop and i_stop < i_start:
            raise ValidationError('Stop time should be after start time')
        if i_start > right_now or (has_stop and i_stop > right_now):
            raise ValidationError('Times should be in the past or present')
        return attrs

    class Meta:
        model = Interval
        fields = '__all__'
