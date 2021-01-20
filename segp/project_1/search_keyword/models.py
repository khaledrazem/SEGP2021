from django.db import models
from paper.models import Paper

# Create your models here.
class Keyword(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    total_publication = models.IntegerField()
    average_reader_count = models.DecimalField(max_digits=10, decimal_places=2)
    score = models.DecimalField(max_digits=10, decimal_places=2)
    growth = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(null=True, blank=True)

class Keyword_Paper(models.Model):
    keyword_id = Keyword.id
    paper_id = Paper.id