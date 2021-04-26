# file created by group
from .models import Topic
from datetime import datetime

# check if data is in database
def isinTopicDB(query):
    if (Topic.objects.filter(name=query).exists()):
        return True
    else:
        return False

# check if data is updated
def isTopicUpdated(query):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    topic = Topic.objects.get(name=query)
    day_diff = (last.date() - topic.last_update).days
    if (day_diff <= 30):
        return True
    else:
        return False

# insert data to database
def insertTopic(query, score):
    topic = Topic(name=query, trend_score=score, last_update=getCurrentTime())
    topic.save()
    print("insert", query)


# update database
def updateTopic(query, score):
    topic = Topic.objects.get(name=query)
    topic.trend_score = score
    topic.last_update = getCurrentTime()
    topic.save()
    print("update", query)

# get data from database
def selectTopic(query):
    result = Topic.objects.get(name=query)
    return result

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time

def checkTopicStatus(query):
    if isinTopicDB(query):
        if (isTopicUpdated(query)==False):
            return 1  # in db but not updated
        else:
            return 2  # in db and is updated
            
    else:
        return 0     #not in db
        