from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from .permissions import (
    AdminOrAuthorCanEdit,
)

from .models import (
    Task,
    Interval,
    User,
)

from .serializers import (
    UserSerializer,
    TaskSerializer,
    IntervalSerializer,
)


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        IsAuthenticated,
    )

    def get_queryset(self):
        """
        Only return info for the currently authenticated user.
        """
        user = self.request.user
        return User.objects.filter(username=user.username)

    @action(methods=['get'], detail=True)
    def tasks(self, request, pk=None):
        queryset = Task.objects.filter(author__pk=pk).order_by('-created')

        context = {'request': request}

        serializer = TaskSerializer(queryset, context=context, many=True)

        return Response(serializer.data)


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    permission_classes = (
        IsAuthenticated,
        AdminOrAuthorCanEdit,
    )

    def get_queryset(self):
        """
        Only return info for the currently authenticated user.
        """
        user = self.request.user
        return Task.objects.filter(author=user)

    @action(methods=['get'], detail=True)
    def intervals(self, request, pk=None):
        queryset = Interval.objects.filter(task__pk=pk).order_by('-created')

        context = {'request': request}

        serializer = IntervalSerializer(queryset, context=context, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super(TaskViewSet, self).perform_create(serializer)

    def perform_destroy(self, instance):
        # Mark task as deleted without actually detroying data
        # items marked for deletion will be deleted at a later time
        instance.deleted = True
        instance.save()


class IntervalViewSet(ModelViewSet):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer

    permission_classes = (
        IsAuthenticated,
        AdminOrAuthorCanEdit,
    )

    def get_queryset(self):
        """
        Only return info for the currently authenticated user.
        """
        user = self.request.user
        taskList = user.tasks.all().values_list('id', flat=True)
        return Interval.objects.filter(task__in=taskList)

    def perform_create(self, serializer):
        # Set the interval's task to running
        task = serializer.validated_data['task']
        task.running = True
        task.save()
        serializer.save(author=self.request.user)
        return super(IntervalViewSet, self).perform_create(serializer)

    def perform_update(self, serializer):
        # Set the interval's task to stopped
        task = serializer.validated_data['task']
        task.running = False
        task.save()
        return super(IntervalViewSet, self).perform_create(serializer)
