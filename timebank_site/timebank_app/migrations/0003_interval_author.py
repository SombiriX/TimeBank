# Generated by Django 2.1.2 on 2018-10-06 07:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('timebank_app', '0002_remove_interval_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='interval',
            name='author',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='intervals', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
