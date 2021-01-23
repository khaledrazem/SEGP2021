from .models import Subcategory
from datetime import datetime

def isinSubcatDB(query):
    if (Subcategory.objects.filter(name = query).exists()):
        return True
    else:
        return False

def isSubcatUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    subcat = Subcategory.objects.get(name=query)
    day_diff = (last.date() - subcat.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False

def insertSubcat(query, score):
    subcat = Subcategory(name=query, trend_score=score, last_update=getCurrentTime())
    subcat.save()

def updateSubcat(query, score):
    subcat = Subcategory.objects.get(name=query)
    subcat.trend_score = score
    subcat.last_update = getCurrentTime()
    subcat.save()
    
def selectSubcate(query):
    result = Subcategory.objects.get(name=query)
    

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time