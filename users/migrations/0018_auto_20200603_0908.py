# Generated by Django 3.0.3 on 2020-06-03 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20200603_0903'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='phone_number',
            new_name='contact',
        ),
    ]
