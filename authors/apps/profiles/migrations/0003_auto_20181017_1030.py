# Generated by Django 2.1.1 on 2018-10-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_profile_favorites'),
    ]

    operations = [
        migrations.AlterField(
            model_name='followinguser',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
