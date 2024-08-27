# Generated by Django 5.0.8 on 2024-08-27 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_userprofile_followed_topics'),
        ('topic', '0016_alter_topicfollow_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnswersFollow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follow_at', models.DateTimeField(auto_now_add=True)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topic.answersroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.userprofile')),
            ],
            options={
                'ordering': ['-follow_at'],
                'unique_together': {('user', 'answer')},
            },
        ),
    ]
