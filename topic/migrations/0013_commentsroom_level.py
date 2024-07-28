# Generated by Django 5.0.7 on 2024-07-26 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("topic", "0012_alter_commentsroom_father_comment_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="commentsroom",
            name="level",
            field=models.IntegerField(
                choices=[(1, "Level 1"), (2, "Level 2")], default=1
            ),
        ),
    ]