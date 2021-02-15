from .models import paper_subcategory_relationship
from .db_paper import *
from subcategory.db_subcategory_query import *
from datetime import datetime

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time


# check if data is in database
def isinDB_Paper_subcategory(paper_title,query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    if query_2==None:
        subcategory_2 = None
    else:
        subcategory_2 = selectSubcat(query_2)
    paper = select_Paper(paper_title)
    if (paper_subcategory_relationship.objects.filter(paper_subcategory_1=subcategory_1, paper_subcategory_2=subcategory_2,paper=paper).exists()):
        #print("T")
        return True
    else:
        """
        if(paper_subcategory_relationship.objects.filter(paper_subcategory_1=subcategory_2, paper_subcategory_2=subcategory_1,paper=paper).exists()):
            return True
        else:
            #print("F")
            return False
        """
        return False

# insert to database
def insert_Paper_subcategory(paper_title,query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    if query_2 == None:
        subcategory_2 = None
    else:
        subcategory_2 = selectSubcat(query_2)
    paper = select_Paper(paper_title)
    new_relation = paper_subcategory_relationship(paper_subcategory_1=subcategory_1, paper_subcategory_2=subcategory_2,paper=paper)
    new_relation.save()
    print("insert new relationship")

# get data from database
def select_Paper_subcategory(paper_title,query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    if query_2 == None:
        subcategory_2 = None
    else:
        subcategory_2 = selectSubcat(query_2)
    paper = select_Paper(paper_title)
    result = paper_subcategory_relationship.objects.get(paper_subcategory_1=subcategory_1, paper_subcategory_2=subcategory_2,paper=paper)
    return result


def store_Paper_subcategory(paper_title,query_1,query_2):
    if (isinDB_Paper_subcategory(paper_title,query_1,query_2) == False):
        insert_Paper_subcategory(paper_title, query_1, query_2)

def get_related_paper_with_subcategory_combination(query_1,query_2):
    subcategory_1 = selectSubcat(query_1)
    if query_2 == None:
        subcategory_2 = None
    else:
        subcategory_2 = selectSubcat(query_2)
    return paper_subcategory_relationship.objects.filter(paper_subcategory_1=subcategory_1, paper_subcategory_2=subcategory_2)

