from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

import django.utils.timezone as timezone

class Post(models.Model):
    title = models.CharField(max_length=140, null=False, blank=False)
    datetime = models.DateTimeField(default=timezone.now, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    text = models.TextField(max_length=140, null=False, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.text
