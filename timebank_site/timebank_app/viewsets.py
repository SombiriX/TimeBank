from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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


class CurrentUserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        IsAuthenticated,
    )

    @action(methods=['get'], detail=True)
    def intervals(self, request, pk=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserSerializer

    permission_classes = (
        IsAdminUser,
    )

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

    @action(methods=['get'], detail=True)
    def intervals(self, request, pk=None):
        queryset = Interval.objects.filter(task__pk=pk).order_by('-created')

        context = {'request': request}

        serializer = IntervalSerializer(queryset, context=context, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super(TaskViewSet, self).perform_create(serializer)


class IntervalViewSet(ModelViewSet):
    queryset = Interval.objects.all()
    serializer_class = IntervalSerializer

    permission_classes = (
        IsAuthenticated,
        AdminOrAuthorCanEdit,
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        return super(IntervalViewSet, self).perform_create(serializer)
