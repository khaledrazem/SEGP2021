from .models import subcategory_combination
from subcategory.db_subcategory_query import *
from datetime import datetime

# check if data is in database
def isinCombDB(query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    if (subcategory_combination.objects.filter(subcategory_1=subcategory_1, subcategory_2=subcategory_2).exists()):
        return True
    elif (subcategory_combination.objects.filter(subcategory_1=subcategory_2, subcategory_2=subcategory_1).exists()):
        return True
    else:
        return False

# check if data is updated
def isCombUpdated(query_1,query_2):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    try:
        comb = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    except:
        comb = subcategory_combination.objects.get(subcategory_1=subcategory_2, subcategory_2=subcategory_1)
    day_diff = (last.date() - comb.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False

# insert to database
def insertComb(query_1,query_2, readercount, authorscore,growth,pie_score,quickScore):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    comb = subcategory_combination(subcategory_1=subcategory_1, subcategory_2=subcategory_2, combination_score=readercount,combination_authorscore=authorscore,combination_growth=growth,combination_pie = pie_score,last_update=getCurrentTime(), quick_search_data=quickScore)
    comb.save()
    print("insert", subcategory_1.name,"and", subcategory_2.name)

# update database
def updateComb(query_1,query_2, readercount, authorscore,growth,pie_score,quickScore):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    try:
        comb = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    except:
        comb = subcategory_combination.objects.get(subcategory_1=subcategory_2, subcategory_2=subcategory_1)
    comb.combination_score = readercount
    comb.combination_authorscore = authorscore
    comb.combination_growth = growth
    comb.combination_pie = pie_score
    comb.last_update = getCurrentTime()
    comb.quick_search_data = quickScore
    comb.save()
    print("update", subcategory_1.name,"and", subcategory_2.name)

# get data from database
def selectComb(query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    subcategory_2 = selectSubcat(query_2)
    try:
        result = subcategory_combination.objects.get(subcategory_1=subcategory_1, subcategory_2=subcategory_2)
    except:
        result = subcategory_combination.objects.get(subcategory_1=subcategory_2, subcategory_2=subcategory_1)
    return result

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time

def checkCombStatus(x,quick):
    if isinCombDB(query_1=x[0],query_2=x[1]):
        comb_result = selectComb(query_1=x[0],query_2=x[1])
        if (isCombUpdated(query_1=x[0],query_2=x[1])==False) or (comb_result.quick_search_data != quick):
            status = 1      # in db but not updated
        else:
            status = 2      # in db and is updated
    else:
        status = 0      # not in db
    print("Status="+str(status))
    return status