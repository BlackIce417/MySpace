# Generated by Django 5.0.7 on 2024-08-22 09:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_userprofile_followed_topics'),
        ('topic', '0015_rename_topicfollows_topicfollow_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicfollow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile'),
        ),
    ]
