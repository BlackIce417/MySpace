# Generated by Django 5.0.8 on 2024-08-27 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topic', '0019_alter_answersfollow_approve_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersfollow',
            name='approve_status',
            field=models.CharField(choices=[('approve', 'approve'), ('disapprove', 'disapprove')], default='none', max_length=12),
        ),
    ]