from .models import paper_keyword_relationship,Paper
from .db_paper import *
from search_keyword.db_keyword_query import *
from datetime import datetime

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time


# check if data is in database
def isinDB_Paper_keyword(paper_title,query_1,query_2):
    keyword_1 =  db_get_keyword_data(query_1)
    if query_2==None:
        keyword_2 = None
    else:
        keyword_2 =  db_get_keyword_data(query_2)
    paper = select_Paper(paper_title)
    if (paper_keyword_relationship.objects.filter(paper_keyword_1=keyword_1, paper_keyword_2=keyword_2,paper=paper).exists()):
        return True
    else:
        return False

# insert to database
def insert_Paper_keyword(paper_title,query_1,query_2):
    keyword_1 =  db_get_keyword_data(query_1)
    if query_2 == None:
        keyword_2 = None
    else:
        keyword_2 =  db_get_keyword_data(query_2)
    paper = select_Paper(paper_title)
    new_relation = paper_keyword_relationship(paper_keyword_1=keyword_1, paper_keyword_2=keyword_2,paper=paper)
    new_relation.save()
    print("insert new relationship")

# get data from database
def select_Paper_keyword(paper_title,query_1,query_2):
    keyword_1 =  db_get_keyword_data(query_1)
    if query_2 == None:
        keyword_2 = None
    else:
        keyword_2 =  db_get_keyword_data(query_2)
    paper = select_Paper(paper_title)
    result = paper_keyword_relationship.objects.get(paper_keyword_1=keyword_1, paper_keyword_2=keyword_2,paper=paper)
    return result


def store_Paper_keyword(paper_title,keyword_1,keyword_2):
    if (isinDB_Paper_keyword(paper_title,keyword_1,keyword_2)==False):
        insert_Paper_keyword(paper_title,keyword_1,keyword_2)

def get_related_paper_with_keyword_combination(query_1,query_2):
    keyword_1 = db_get_keyword_data(query_1)
    if query_2 == None:
        keyword_2 = None
    else:
        keyword_2 = db_get_keyword_data(query_2)
    return paper_keyword_relationship.objects.filter(paper_keyword_1=keyword_1, paper_keyword_2=keyword_2)
