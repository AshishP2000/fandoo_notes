from django.db import models

from user.models import User


# Create your models here.

class Labels(models.Model):
    title = models.TextField()
    color = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Notes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.TextField()
    note_body = models.TextField()
    collaborator = models.ManyToManyField(User, related_name='collaborator')
    label = models.ManyToManyField(Labels, related_name='label')


