# Generated by Django 5.0.6 on 2024-06-25 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_alter_userprofile_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="media/images/avatars/default-avatar.png",
                upload_to="media/images/avatars/",
            ),
        ),
    ]
