from .models import Subcategory
from datetime import datetime

"""
def isinDB(query):
    try:
        test = Subcategory.objects.get(name=name)
    except Subcategory.DoesNotExist:
        test = None
        
    return test

"""





def isinDB(query):
    if (Subcategory.objects.filter(name = query).exists()):
        return True
    else:
        return False

def isUpdated(query):
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
    








"""
def storeSubcat(query):
    if isinDB(query.name):
        test = Subcategory.objects.get(name=query.name)
        if (~isUpdated(test)):
            test.last_update = getCurrentTime()
            test.trend_scor = query.trend_scor
            test.save()
    else:
        keyword = query
        keyword.last_update = getCurrentTime()
        keyword.save()



def isinDB(query):
    if (Subcategory.objects.filter(name = query).exists()):
        return True
    else:
        return False

def isUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    day_diff = (last.date() - query.last_update).days
    if (day_diff <= 14):
        return True
    else :
        return False

def isValid(query):
    if (isinDB(query)):
        entity = Subcategory.objects.get(name=query)
        if (isUpdated(entity)):
            return True
    return False

def get_data(query_name):
    if isValid(query_name.title()):
        result = subcategory.objects.get(name=query_name.title())
        return result
    else:
        return False
"""