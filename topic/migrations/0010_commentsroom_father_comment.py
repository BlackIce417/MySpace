# Generated by Django 5.0.7 on 2024-07-23 16:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("topic", "0009_alter_answersroom_options_alter_commentsroom_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commentsroom",
            name="father_comment",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="son_comment",
                to="topic.commentsroom",
                verbose_name="father comment",
            ),
        ),
    ]
