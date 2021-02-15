from .models import Keyword
from datetime import datetime

def storeKeyword(query):
    if isinDB(query.name):
        test = Keyword.objects.get(name=query.name)
        if ((isUpdated(test)==False) or (query.quick_search_data != test.quick_search_data)):
            test.last_update = getCurrentTime()
            test.score = query.score
            test.total_publication = query.total_publication
            test.average_reader_count = query.average_reader_count
            test.growth = query.growth
            test.quick_search_data = query.quick_search_data
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
    if (Keyword.objects.filter(name = query).exists()):
        # print(query,"-> can be found")
        return True
    else:
        # print(query, "-> can't be found")
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
        entity = Keyword.objects.get(name=query)
        if (isUpdated(entity)):
            return True
    return False

def get_keyword_data(query_name,quickSearch):
    if isValid(query_name.title()):
        result = Keyword.objects.get(name=query_name.title())
        if (result.quick_search_data == quickSearch):
            return result
        else:
            return False
    else:
        return False

def db_get_keyword_data(query_name):
    if isValid(query_name.title()):
        result = Keyword.objects.get(name=query_name.title())
        return result
    else:
        return False

