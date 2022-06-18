from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    name = models.CharField(max_length=55)
    description = models.CharField(max_length=500)
    date = models.DateField()
    time = models.TimeField()
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='event')

    imgAddress = models.CharField(max_length=2000)
    extraLink = models.CharField(max_length=500)
    city = models.ManyToManyField("City", related_name="events")
