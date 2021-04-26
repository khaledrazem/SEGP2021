# file created by group
from django.db import models
from topic.models import Topic

# Create your models here.
class topic_combination(models.Model):
    class Meta:
        unique_together = (('topic_1', 'topic_2'),)

    topic_1 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subcategory_1")
    topic_2 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="subcategory_2")
    combination_score = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_authorscore = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_growth = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    combination_pie = models.DecimalField(max_digits=10, decimal_places=5,default=0)
    last_update = models.DateField(null=True, blank=True)