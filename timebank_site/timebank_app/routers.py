from rest_framework.routers import DefaultRouter

from .viewsets import (
    IntervalViewSet,
    TaskViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register(r'interval', IntervalViewSet)
router.register(r'task', TaskViewSet)
router.register(r'users_api', UserViewSet)
