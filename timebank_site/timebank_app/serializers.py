from django.db.models import F, Sum
from django.utils import timezone
from .models import (
    Task,
    Interval,
    User,
)
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
    SerializerMethodField,
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
        else:
            return None

    def get_runtime(self, instance):
        # Calculate how long the tasks has run for
        res = Interval.objects.filter(task__pk=instance.pk).order_by('-created')
        recorded_time = res\
            .annotate(task_duration=F('stop') - F('start'))\
            .aggregate(total_duration=Sum(F('task_duration')))\
            .get('total_duration', None)

        active_time = 0
        if instance.running:
            # Get the most recent interval and calculate the runtime
            # at this moment
            running_interval = res[0]
            active_time = timezone.now() - running_interval.start

        return (active_time + recorded_time) if recorded_time else active_time

    def get_validation_exclusions(self, *args, **kwargs):
        # exclude the author field as we supply it later on in the
        # corresponding view based on the http request
        exclusions = super(
            TaskSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['author']

    def to_representation(self, instance):
        # Convert time_budget HH:MM:SS to HH:MM
        ret = super().to_representation(instance)
        ret['time_budget'] = ret['time_budget'][0:5]
        return ret

    def to_internal_value(self, data):
        # Convert time_budget from HH:MM to HH:MM:SS
        data['time_budget'] += ":00"
        ret = super().to_internal_value(data)
        return ret

    class Meta:
        model = Task
        fields = '__all__'


class IntervalSerializer(ModelSerializer):

    class Meta:
        model = Interval
        fields = '__all__'
