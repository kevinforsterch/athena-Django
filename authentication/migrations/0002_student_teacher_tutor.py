# Generated by Django 2.1.5 on 2019-02-09 08:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('edu', '0004_auto_20190209_1117'),
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group',
                 models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='student',
                                   to='edu.StudentGroup')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='student',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjects', models.ManyToManyField(related_name='teacher', to='edu.Subject')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='teacher',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='tutor',
                                              to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
