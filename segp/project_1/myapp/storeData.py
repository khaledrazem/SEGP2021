from search_keyword.models import Keyword
from datetime import datetime

def store(query,avgRCS):
    mystring = str(query)
    
    if mystring[2] == " ":
        temp = mystring[3:]
    else:
        temp = mystring[2:]
    
    name = temp[:-3]

    try:
        test = Keyword.objects.get(name=name)
    except Keyword.DoesNotExist:
        test = None
    
    if test == None:
        keyword = Keyword(name=name, score=avgRCS, last_update=getCurrentTime())
        keyword.save()
    else:
        last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
        day_diff = (last.date() - test.last_update).days
        if day_diff > 7:
            test.last_update = getCurrentTime()
            test.score = avgRCS
            test.save()

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time