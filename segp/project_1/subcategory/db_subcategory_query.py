from .models import subcategory
from datetime import datetime


def store(query):
    if isinDB(query.name):
        test = subcategory.objects.get(name=query.name)
        if (~isUpdated(test)):
            test.last_update = getCurrentTime()
            test.trend_scor = query.trend_scor
            test.save()
    else:
        keyword = query
        keyword.last_update = getCurrentTime()
        keyword.save()

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time

def isinDB(query):
    if (subcategory.objects.filter(name = query).exists()):
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
        entity = subcategory.objects.get(name=query)
        if (isUpdated(entity)):
            return True
    return False

def get_data(query_name):
    if isValid(query_name.title()):
        result = subcategory.objects.get(name=query_name.title())
        return result
    else:
        return False