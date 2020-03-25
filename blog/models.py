from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


class post(models.Model):
    title = models.CharField(max_length=100, default="  ")
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.content  # print out title of objects instead of number of objects returned

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
