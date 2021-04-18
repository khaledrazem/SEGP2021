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
    if (day_diff <= 30):
        return True
    else:
        return False

# insert data to database
def insertSubcat(query, score):
    subcat = Subcategory(name=query, trend_score=score, last_update=getCurrentTime())
    subcat.save()
    print("insert", query)


# update database
def updateSubcat(query, score):
    subcat = Subcategory.objects.get(name=query)
    subcat.trend_score = score
    subcat.last_update = getCurrentTime()
    subcat.save()
    print("update", query)

# get data from database
def selectSubcat(query):
    result = Subcategory.objects.get(name=query)
    return result

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time

def checkSubcatStatus(query):
    if isinSubcatDB(query):
        if (isSubcatUpdated(query)==False):
            return 1  # in db but not updated
        else:
            return 2  # in db and is updated
            
    else:
        return 0     #not in db
        