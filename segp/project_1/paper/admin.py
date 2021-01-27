from django.contrib import admin
from .models import Paper,paper_keyword_relationship

# Register your models here.
admin.site.register(Paper)
admin.site.register(paper_keyword_relationship)
