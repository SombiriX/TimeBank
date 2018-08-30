from django.contrib import admin

from .models import (
    Interval,
    Task,
    User,
)

admin.site.register(Interval)
admin.site.register(Task)
admin.site.register(User)
