from .models import Combination
from datetime import datetime

# check if data is in database
def isinCombDB(query):
    if (Combination.objects.filter(name = query).exists()):
        return True
    else:
        return False

# check if data is updated
def isCombUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    comb = Combination.objects.get(name=query)
    day_diff = (last.date() - comb.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False

# insert to database
def insertComb(query, score):
    comb = Combination(name=query, combination_score=score, last_update=getCurrentTime())
    comb.save()
    print("insert", query)

# update database
def updateComb(query, score):
    comb = Combination.objects.get(name=query)
    comb.combination_score = score
    comb.last_update = getCurrentTime()
    comb.save()
    print("update", query)

# get data from database
def selectComb(query):
    result = Combination.objects.get(name=query)
    this_reader = result.combination_score
    return this_reader
    
def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time