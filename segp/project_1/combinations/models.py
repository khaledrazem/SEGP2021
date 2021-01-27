from django.db import models
from search_keyword.models import Keyword

# Create your models here.
class Combination(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    combination_score = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(null=True, blank=True)

class keyword_combination(models.Model):
    class Meta:
        unique_together = (('keyword_1',
                            'keyword_2'),)

    keyword_1 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="keyword_1")
    keyword_2 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="keyword_2")
    total_publication = models.IntegerField()
    average_reader_count = models.DecimalField(max_digits=10, decimal_places=2)
    score = models.DecimalField(max_digits=10, decimal_places=2)
    growth = models.DecimalField(max_digits=10, decimal_places=2)
    last_update = models.DateField(null=True, blank=True)