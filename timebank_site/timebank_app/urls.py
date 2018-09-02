from django.urls import path
from .routers import router
from .views import appView

urlpatterns = [
    path('', appView.as_view(), name='index'),
]

urlpatterns += router.urls
