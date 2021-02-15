from django.db import models
from search_keyword.models import Keyword
from subcategory.models import Subcategory
# from subcategory.models import


# Create your models here.
class Paper(models.Model):
    name = models.CharField(max_length=500,primary_key=True)
    reader_count = models.IntegerField()
    link = models.CharField(max_length=500)
    year_published = models.IntegerField()
    last_update = models.DateField(null=True, blank=True)

class paper_keyword_relationship(models.Model):
    class Meta:
        unique_together = (('paper_keyword_1',
                            'paper_keyword_2',
                            'paper'),)
    paper_keyword_1 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="paper_keyword_1", db_constraint=False)
    paper_keyword_2 = models.ForeignKey(Keyword, on_delete=models.CASCADE, related_name="paper_keyword_2", null=True, blank=True, db_constraint=False)
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE, related_name="paper_of_keywords")

class paper_subcategory_relationship(models.Model):
    class Meta:
        unique_together = (('paper_subcategory_1',
                            'paper_subcategory_2',
                            'paper'))
    paper_subcategory_1 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="paper_subcategory_1", db_constraint=False)
    paper_subcategory_2 = models.ForeignKey(Subcategory, on_delete=models.CASCADE, related_name="paper_subcategory_2", null=True, blank=True, db_constraint=False)
    paper = models.ForeignKey(Paper,on_delete=models.CASCADE, related_name="paper_of_subcategories")