# Generated by Django 2.1.7 on 2019-03-29 15:19

import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('works', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='task',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False),
        ),
    ]
