from django.db import models
from search_keyword.models import Keyword
from subcategory.models import Subcategory

# Create your models here.

class keyword_combination(models.Model):
    class Meta:
        unique_together = (('keyword_1',
                            'keyword_2'),)

    keyword_1 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="keyword_1", db_constraint=False)
    keyword_2 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="keyword_2", db_constraint=False)
    total_publication = models.IntegerField()
    average_reader_count = models.DecimalField(max_digits=10, decimal_places=2)
    score = models.DecimalField(max_digits=10, decimal_places=2)
    growth = models.DecimalField(max_digits=10, decimal_places=2)
    quick_search_data = models.BooleanField(null=True, blank=True)
    last_update = models.DateField(null=True, blank=True)

class subcategory_combination(models.Model):
    class Meta:
        unique_together = (('subcategory_1',
                            'subcategory_2'),)

    subcategory_1 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="subcategory_1")
    subcategory_2 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="subcategory_2")
    combination_score = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_authorscore = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_growth = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    quick_search_data = models.BooleanField(null=True, blank=True)
    last_update = models.DateField(null=True, blank=True)