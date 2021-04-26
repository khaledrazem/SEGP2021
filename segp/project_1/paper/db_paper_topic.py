# file created by group
from .models import paper_topic_relationship
from .db_paper import *
from topic.db_topic_query import *
from datetime import datetime

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time


# check if data is in database
def isinDB_Paper_topic(paper_title,query_1,query_2):
    topic_1 = selectTopic(query_1)
    if query_2==None:
        topic_2 = None
    else:
        topic_2 = selectTopic(query_2)
    paper = select_Paper(paper_title)
    if (paper_topic_relationship.objects.filter(paper_topic_1=topic_1, paper_topic_2=topic_2,paper=paper).exists()):
        return True
    else:
        return False

# insert to database
def insert_Paper_topic(paper_title,query_1,query_2):
    topic_1 = selectTopic(query_1)
    if query_2 == None:
        topic_2 = None
    else:
        topic_2 = selectTopic(query_2)
    paper = select_Paper(paper_title)
    new_relation = paper_topic_relationship(paper_topic_1=topic_1, paper_topic_2=topic_2,paper=paper)
    new_relation.save()
    print("insert new relationship")

# get data from database
def select_Paper_topic(paper_title,query_1,query_2):
    topic_1 = selectTopic(query_1)
    if query_2 == None:
        topic_2 = None
    else:
        topic_2 = selectTopic(query_2)
    paper = select_Paper(paper_title)
    result = paper_topic_relationship.objects.get(paper_topic_1=topic_1, paper_topic_2=topic_2,paper=paper)
    return result


def store_Paper_topic(paper_title,query_1,query_2):
    if (isinDB_Paper_topic(paper_title,query_1,query_2) == False):
        insert_Paper_topic(paper_title, query_1, query_2)

def get_related_paper_with_topic_combination(query_1,query_2):
    topic_1 = selectTopic(query_1)
    if query_2 == None:
        topic_2 = None
    else:
        topic_2 = selectTopic(query_2)
    return paper_topic_relationship.objects.filter(paper_topic_1=topic_1, paper_topic_2=topic_2)
    

def get_related_paper_with_keyword(query_1,query_2):
    topic_1 = selectTopic(query_1)
    if paper_topic_relationship.objects.filter(paper_topic_1=topic_1).exists():
        results = paper_topic_relationship.objects.filter(paper_topic_1=topic_1)
    else:
        results = paper_topic_relationship.objects.filter(paper_topic_2=topic_1)
    return results
