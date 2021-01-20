from django.db import models
from paper_author.models import Author

# Create your models here.
class Paper(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=500)
    num_of_citation = models.IntegerField
    last_update = models.DateField(null=True, blank=True)

class Author_Paper(models.Model):
    paper_id = Paper.id
    author_id = Author.id