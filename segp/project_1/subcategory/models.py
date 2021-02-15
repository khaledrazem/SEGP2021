from django.db import models

# Create your models here.
class Subcategory(models.Model):
    name = models.CharField(max_length=500)
    trend_score = models.DecimalField(max_digits=10, decimal_places=2)
    quick_search_data = models.BooleanField(null=True, blank=True)
    last_update = models.DateField(null=True, blank=True)
