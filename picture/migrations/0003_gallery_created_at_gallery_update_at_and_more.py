# Generated by Django 5.0.8 on 2024-09-11 14:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('picture', '0002_alter_gallery_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='gallery',
            name='update_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='picture',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
