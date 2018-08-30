from rest_framework.serializers import (
    HyperlinkedIdentityField,
    HyperlinkedRelatedField,
    ModelSerializer,
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

    def get_validation_exclusions(self, *args, **kwargs):
        # exclude the author field as we supply it later on in the
        # corresponding view based on the http request
        exclusions = super(
            TaskSerializer, self).get_validation_exclusions(*args, **kwargs)
        return exclusions + ['author']

    class Meta:
        model = Task
        fields = '__all__'


class IntervalSerializer(ModelSerializer):
    task = HyperlinkedRelatedField(view_name='task-detail', read_only=True)

    class Meta:
        model = Interval
        fields = '__all__'
