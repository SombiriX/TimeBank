from django.urls import path
from .routers import router
from .views import AppView, current_user

urlpatterns = [
    path('', AppView.as_view(), name='index'),
    path('user/', current_user, name='currentUser'),
]

urlpatterns += router.urls
