# file created by django and modified by group
from django.db import models

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=500)
    trend_score = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(null=True, blank=True)
