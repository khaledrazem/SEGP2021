from django.db import models

# Create your models here.
class Author(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    num_of_publication = models.IntegerField
    last_update = models.DateField(null=True, blank=True)