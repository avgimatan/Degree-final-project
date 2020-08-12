# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-01 10:04
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('avatar_name', models.CharField(max_length=255, unique=True)),
                ('avatar_password', models.CharField(max_length=255)),
                ('avatar_email', models.CharField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='avatars', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='avatar',
            unique_together=set([('user', 'avatar_name', 'avatar_password', 'avatar_email', 'created_at')]),
        ),
    ]
