# Generated by Django 2.1 on 2018-09-13 04:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timebank_app', '0005_auto_20180908_0655'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='is_complete',
            new_name='complete',
        ),
        migrations.AddField(
            model_name='task',
            name='running',
            field=models.BooleanField(default=False),
        ),
    ]
