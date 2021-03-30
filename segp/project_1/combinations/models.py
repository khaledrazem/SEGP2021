from django.db import models
from subcategory.models import Subcategory

# Create your models here.
class subcategory_combination(models.Model):
    class Meta:
        unique_together = (('subcategory_1',
                            'subcategory_2'),)

    subcategory_1 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="subcategory_1")
    subcategory_2 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="subcategory_2")
    combination_score = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_authorscore = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_growth = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_pie = models.DecimalField(max_digits=10, decimal_places=5,default=0)
    quick_search_data = models.BooleanField(null=True, blank=True)
    last_update = models.DateField(null=True, blank=True)