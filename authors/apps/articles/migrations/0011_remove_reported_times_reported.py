# Generated by Django 2.1.1 on 2018-10-18 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0010_article_times_reported'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reported',
            name='times_reported',
        ),
    ]
