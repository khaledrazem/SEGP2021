from .models import keyword_combination
from datetime import datetime
from search_keyword.db_keyword_query import *
from .db_combination_query import *


# check if data is in database
def isinDB_KeywordCombination(query_1,query_2):
    keyword_1 = get_keyword_data(query_1)
    keyword_2 = get_keyword_data(query_2)
    if (keyword_combination.objects.filter(keyword_1=keyword_1,keyword_2=keyword_2).exists()):
        return True
    elif (keyword_combination.objects.filter(keyword_1=keyword_2,keyword_2=keyword_1).exists()):
        return True
    else:
        return False


# check if data is updated
def isUpdated_KeywordCombination(query_1,query_2):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    keyword_1 = get_keyword_data(query_1)
    keyword_2 = get_keyword_data(query_2)
    if (keyword_combination.objects.filter(keyword_1=keyword_1, keyword_2=keyword_2).exists()):
        result = keyword_combination.objects.get(keyword_1=keyword_1, keyword_2=keyword_2)
    elif (keyword_combination.objects.filter(keyword_1=keyword_2, keyword_2=keyword_1).exists()):
        result = keyword_combination.objects.get(keyword_1=keyword_1, keyword_2=keyword_2)
    day_diff = (last.date() - result.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False


# insert to database
def insert_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth):
    keyword_1 = get_keyword_data(query_1)
    keyword_2 = get_keyword_data(query_2)
    comb = keyword_combination(keyword_1=keyword_1, keyword_2=keyword_2, average_reader_count=average_reader_count, score=round(round(average_reader_count+1, 2) / (total_publication+1), 2), total_publication=total_publication, growth=growth, last_update=getCurrentTime())
    comb.save()
    print("insert", keyword_1,keyword_2)


# update database
def update_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth):
    result = select_KeywordCombination(query_1,query_2)
    result.average_reader_count = average_reader_count
    result.total_publication = total_publication
    result.growth = growth
    result.score = round(round(average_reader_count+1, 2) / (total_publication+1), 2)
    result.last_update = getCurrentTime()
    result.save()
    print("update",  query_1,query_2)


# get data from database
def select_KeywordCombination(query_1,query_2):
    print()
    print(query_1, query_2)
    if isValid_KeywordCombination(query_1,query_2):
        keyword_1 = get_keyword_data(query_1)
        keyword_2 = get_keyword_data(query_2)
        if (keyword_combination.objects.filter(keyword_1=keyword_1, keyword_2=keyword_2).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_1,keyword_2=keyword_2)
        elif (keyword_combination.objects.filter(keyword_1=keyword_2, keyword_2=keyword_1).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_1, keyword_2=keyword_2)
        return result
    else:
        return False

def isValid_KeywordCombination(query_1,query_2):
    if (isinDB_KeywordCombination(query_1,query_2)):
        if (isUpdated_KeywordCombination(query_1,query_2)):
            return True
    return False

def store_KeywordCombination(query_1, query_2, average_reader_count, total_publication, growth):
    if isinDB_KeywordCombination(query_1,query_2):
        if (~ isUpdated_KeywordCombination(query_1,query_2)):
            print("x updated")
            update_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth)
    else:
        insert_KeywordCombination(query_1, query_2, average_reader_count, total_publication, growth)
