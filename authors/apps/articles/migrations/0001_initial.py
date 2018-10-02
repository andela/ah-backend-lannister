# Generated by Django 2.1.1 on 2018-10-08 15:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updatedAt', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('createdAt', models.DateTimeField(auto_created=True, default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('body', models.TextField()),
                ('favorited', models.BooleanField(default=False)),
                ('favoritesCount', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['author', '-createdAt'],
                'get_latest_by': 'createdAt',
            },
        ),
    ]