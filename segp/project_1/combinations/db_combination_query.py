from .models import Combination
from datetime import datetime

"""
def isinDB(query):
    try:
        test = Combination.objects.get(name=name)
    except Combination.DoesNotExist:
        test = None
        
    return test

"""





def isinCombDB(query):
    if (Combination.objects.filter(name = query).exists()):
        return True
    else:
        return False

def isCombUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    comb = Combination.objects.get(name=query)
    day_diff = (last.date() - comb.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False

def insertComb(query, score):
    comb = Combination(name=query, combination_score=score, last_update=getCurrentTime())
    comb.save()

def updateComb(query, score):
    comb = Combination.objects.get(name=query)
    comb.combination_score = score
    comb.last_update = getCurrentTime()
    comb.save()
    
def selectComb(query):
    result = Combination.objects.get(name=query)
    

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time
    








"""
def storecomb(query):
    if isinDB(query.name):
        test = Combination.objects.get(name=query.name)
        if (~isUpdated(test)):
            test.last_update = getCurrentTime()
            test.trend_scor = query.trend_scor
            test.save()
    else:
        keyword = query
        keyword.last_update = getCurrentTime()
        keyword.save()



def isinDB(query):
    if (Combination.objects.filter(name = query).exists()):
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
        entity = Combination.objects.get(name=query)
        if (isUpdated(entity)):
            return True
    return False

def get_data(query_name):
    if isValid(query_name.title()):
        result = Combination.objects.get(name=query_name.title())
        return result
    else:
        return False
"""