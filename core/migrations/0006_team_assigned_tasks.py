# Generated by Django 3.2.5 on 2022-05-05 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20220505_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='assigned_tasks',
            field=models.ManyToManyField(to='core.Task'),
        ),
    ]
