from django.db import models


# Create your models here.
class Keyword(models.Model):
    name = models.CharField(max_length=500,primary_key=True)
    keyword_score = models.DecimalField(max_digits=10, decimal_places=2)
    keyword_authorscore = models.DecimalField(max_digits=10, decimal_places=2)
    keyword_growth = models.DecimalField(max_digits=10, decimal_places=2)
    quick_search_data = models.BooleanField(null=True,blank=True)
    last_update = models.DateField(null=True, blank=True)

