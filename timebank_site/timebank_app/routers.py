from rest_framework.routers import DefaultRouter

from .viewsets import (
    IntervalViewSet,
    TaskViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register(r'Interval', IntervalViewSet)
router.register(r'Task', TaskViewSet)
router.register(r'User', UserViewSet)
