from .models import Subcategory
from datetime import datetime


# check if data is in database
def isinSubcatDB(query):
    if (Subcategory.objects.filter(name=query).exists()):
        return True
    else:
        return False

# check if data is updated
def isSubcatUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    subcat = Subcategory.objects.get(name=query)
    day_diff = (last.date() - subcat.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False


# insert data to database
def insertSubcat(query, score, quickScore):
    subcat = Subcategory(name=query, trend_score=score, last_update=getCurrentTime())
    subcat.quick_search_data = quickScore
    subcat.save()
    print("insert", query)


# update database
def updateSubcat(query, score, quickScore):
    subcat = Subcategory.objects.get(name=query)
    subcat.trend_score = score
    subcat.last_update = getCurrentTime()
    subcat.quick_search_data = quickScore
    subcat.save()

# get data from database
def selectSubcat(query):
    result = Subcategory.objects.get(name=query)
    return result

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time
