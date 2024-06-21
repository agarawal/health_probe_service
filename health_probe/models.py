# health_probe_service/probe/models.py

from django.db import models

class Probe(models.Model):
    url = models.URLField(unique=True)
    duration = models.IntegerField()

    def __str__(self):
        return self.url