# Generated by Django 3.0.5 on 2020-06-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_remove_profile_fc_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='org',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
