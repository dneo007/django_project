# Generated by Django 3.0.3 on 2020-03-29 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_delete_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='fc_pic',
            field=models.ImageField(null=True, upload_to='pics'),
        ),
    ]
