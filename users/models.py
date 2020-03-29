from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils.translation import gettext_lazy as _
from django import forms
import os


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user, filename)


class Profile(models.Model):
    fc = models.BooleanField(default=False)  # Enable FaceID
    fc_setup = models.BooleanField(default=False)  # if FaceID has been set up or not
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    fc_pic = models.ImageField(null=True, upload_to='face_images')

    def __str__(self):
        return f'{self.user.username}''s Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)


class FcPic(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    pic = models.ImageField(null=True, upload_to='face_images')

    def __str__(self):
        return f'{self.profile.user.username}'

