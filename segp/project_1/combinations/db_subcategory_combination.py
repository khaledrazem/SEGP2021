from .models import subcategory_combination
from subcategory.db_subcategory_query import *
from datetime import datetime

# check if data is in database
def isinCombDB(query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    if (subcategory_combination.objects.filter(subcategory_1=subcategory_1, subcategory_2=subcategory_2).exists()):
        return True
    else:
        return False

# check if data is updated
def isCombUpdated(query_1,query_2):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    comb = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    day_diff = (last.date() - comb.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False

# insert to database
def insertComb(query_1,query_2, readercount, authorscore,growth,quickScore):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    comb = subcategory_combination(subcategory_1=subcategory_1, subcategory_2=subcategory_2, combination_score=readercount,combination_authorscore=authorscore,combination_growth=growth, last_update=getCurrentTime(), quick_search_data=quickScore)
    comb.save()
    print("insert", subcategory_1.name,"and", subcategory_2.name)

# update database
def updateComb(query_1,query_2, readercount, authorscore,growth,quickScore):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    comb = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    comb.combination_score = readercount
    comb.combination_authorscore = authorscore
    comb.combination_growth = growth
    comb.last_update = getCurrentTime()
    comb.quick_search_data = quickScore
    comb.save()
    print("update", subcategory_1.name,"and", subcategory_2.name)

# get data from database
def selectComb(query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    result = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    return result

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time
