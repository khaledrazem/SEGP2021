# file created by django and modified by group
from django.db import models
from topic.models import Topic

# Create your models here.
class Paper(models.Model):
    name = models.CharField(max_length=500,primary_key=True)
    reader_count = models.IntegerField()
    link = models.CharField(max_length=500)
    year_published = models.IntegerField()
    last_update = models.DateField(null=True, blank=True)


class paper_topic_relationship(models.Model):
    class Meta:
        unique_together = (('paper_topic_1',
                            'paper_topic_2',
                            'paper'))
    paper_topic_1 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="paper_subcategory_1", db_constraint=False)
    paper_topic_2 = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name="paper_subcategory_2", null=True, blank=True, db_constraint=False)
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE, related_name="paper_of_subcategories")