# Generated by Django 3.2.5 on 2022-05-05 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20220505_1813'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='target_date',
            field=models.DateField(null=True),
        ),
    ]
