from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models import Avg


class post(models.Model):
    rating = models.IntegerField(default=0)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    # def getavg(self):
    # self.all().aggregate(Avg('rating'))

    def __str__(self):
        return self.content  # print out title of objects instead of number of objects returned

    def get_absolute_url(self):
        return reverse('blog-home')
