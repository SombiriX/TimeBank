from django.urls import path
from .routers import router
from . import views

urlpatterns = [
    path('', views.index, name='index'),
]

urlpatterns += router.urls
