# Generated by Django 5.0.6 on 2024-06-25 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_alter_userprofile_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="main/images/avatars/default-avatar.png",
                upload_to="main/images/avatars/",
            ),
        ),
    ]
