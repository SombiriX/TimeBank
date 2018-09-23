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
        # exclude the author field as we supply it later on in the
        # corresponding view based on the http request
        exclusions = super(
            TaskSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['author']

    def validate(self, attrs):
        # Verify that required fields are properly formatted
        # TODO remove fields which should not be set manually eg 'running'
        t_name = attrs.get('task_name', None)
        t_budget = attrs.get('time_budget', None)

        if t_name in ('', None) or not isinstance(t_name, str):
            raise ValidationError('A valid task_name is required')
        if t_budget is not None and not isinstance(t_budget, int):
            raise ValidationError(
                'Time budget should be integer seconds'
            )
        return attrs

    class Meta:
        model = Task
        fields = '__all__'


class IntervalSerializer(ModelSerializer):

    class Meta:
        model = Interval
        fields = '__all__'
