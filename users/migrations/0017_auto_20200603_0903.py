# Generated by Django 3.0.3 on 2020-06-03 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_profile_fc_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='job_title',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='organization',
            field=models.CharField(default=' ', max_length=100),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(default=' ', max_length=12),
        ),
    ]
