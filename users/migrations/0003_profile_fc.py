# Generated by Django 3.0.3 on 2020-03-16 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200311_0321'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fc',
            field=models.BooleanField(default=False),
        ),
    ]