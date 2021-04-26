# file created by group
from .models import topic_combination
from topic.db_topic_query import *
from datetime import datetime

# check if data is in database
def isinCombDB(query_1,query_2):
    topic_1 = selectTopic(query_1)
    topic_2 = selectTopic(query_2)
    if (topic_combination.objects.filter(topic_1=topic_1, topic_2=topic_2).exists()):
        return True
    elif (topic_combination.objects.filter(topic_1=topic_2, topic_2=topic_1).exists()):
        return True
    else:
        return False

# check if data is updated
def isCombUpdated(query_1,query_2):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    topic_1 = selectTopic(query_1)
    topic_2 = selectTopic(query_2)
    try:
        comb = topic_combination.objects.get(topic_1=topic_1, topic_2=topic_2)
    except:
        comb = topic_combination.objects.get(topic_1=topic_2, topic_2=topic_1)
    day_diff = (last.date() - comb.last_update).days
    if (day_diff <= 30):
        return True
    else:
        return False

# insert to database
def insertComb(query_1,query_2, readercount, authorscore,growth,pie_score):
    topic_1 = selectTopic(query_1)
    topic_2 = selectTopic(query_2)
    comb = topic_combination(topic_1=topic_1, topic_2=topic_2, combination_score=readercount,combination_authorscore=authorscore,combination_growth=growth,combination_pie = pie_score,last_update=getCurrentTime())
    comb.save()
    print("insert", topic_1.name,"and", topic_2.name)

# update database
def updateComb(query_1,query_2, readercount, authorscore,growth,pie_score):
    topic_1 = selectTopic(query_1)
    topic_2 = selectTopic(query_2)
    try:
        comb = topic_combination.objects.get(topic_1=topic_1, topic_2=topic_2)
    except:
        comb = topic_combination.objects.get(topic_1=topic_2, topic_2=topic_1)
    comb.combination_score = readercount
    comb.combination_authorscore = authorscore
    comb.combination_growth = growth
    comb.combination_pie = pie_score
    comb.last_update = getCurrentTime()
    comb.save()
    print("update", topic_1.name,"and", topic_2.name)

# get data from database
def selectComb(query_1,query_2):
    topic_1 = selectTopic(query_1)
    topic_2 = selectTopic(query_2)
    try:
        result = topic_combination.objects.get(topic_1=topic_1, topic_2=topic_2)
    except:
        result = topic_combination.objects.get(topic_1=topic_2, topic_2=topic_1)
    return result

# get the current date
def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time

# check status of combination in database
def checkCombStatus(x):
    if isinCombDB(query_1=x[0],query_2=x[1]):
        comb_result = selectComb(query_1=x[0],query_2=x[1])
        if (isCombUpdated(query_1=x[0],query_2=x[1])==False):
            status = 1      # in db but not updated
        else:
            status = 2      # in db and is updated
    else:
        status = 0      # not in db
    return status