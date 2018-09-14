from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
    SerializerMethodField,
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

    def get_running_interval(self, instance):
        # Returns the most recent interval related to the task
        if instance.running:
            most_recent_interval = Interval.objects.filter(
                task__pk=instance.pk).order_by('-created')[0]
            return IntervalSerializer(most_recent_interval).data
        else:
            return None

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
