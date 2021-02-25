from .models import keyword_combination
from search_keyword.db_keyword_query import *
from .db_subcategory_combination import *


# check if data is in database
def isinDB_KeywordCombination(query_1,query_2):
    keyword_1 = db_get_keyword_data(query_1)
    keyword_2 = db_get_keyword_data(query_2)
    if (keyword_combination.objects.filter(keyword_1=keyword_1,keyword_2=keyword_2).exists()):
        return True
    elif (keyword_combination.objects.filter(keyword_1=keyword_2,keyword_2=keyword_1).exists()):
        return True
    else:
        return False


# check if data is updated
def isUpdated_KeywordCombination(query_1,query_2):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    keyword_1 = db_get_keyword_data(query_1)
    keyword_2 = db_get_keyword_data(query_2)
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
def insert_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth,quickSearch):
    keyword_1 = db_get_keyword_data(query_1)
    keyword_2 = db_get_keyword_data(query_2)
    comb = keyword_combination(keyword_1=keyword_1, keyword_2=keyword_2, average_reader_count=average_reader_count, score=round(round(average_reader_count+1, 2) / (total_publication+1), 2), total_publication=total_publication, growth=growth, quick_search_data=quickSearch, last_update=getCurrentTime())
    comb.save()
    print("insert", keyword_1,keyword_2)


# update database
def update_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth,quickSearch):
    keyword_1 = db_get_keyword_data(query_1)
    keyword_2 = db_get_keyword_data(query_2)
    if (keyword_combination.objects.filter(keyword_1=keyword_1, keyword_2=keyword_2).exists()):
        result = keyword_combination.objects.get(keyword_1=keyword_1, keyword_2=keyword_2)
    elif (keyword_combination.objects.filter(keyword_1=keyword_2, keyword_2=keyword_1).exists()):
        result = keyword_combination.objects.get(keyword_1=keyword_2, keyword_2=keyword_1)
    result.average_reader_count = average_reader_count
    result.total_publication = total_publication
    result.growth = growth
    result.score = round(round(average_reader_count+1, 2) / (total_publication+1), 2)
    result.last_update = getCurrentTime()
    result.quick_search_data = quickSearch
    result.save()
    print("update",  query_1,query_2)


# get data from database
def select_KeywordCombination(query_1,query_2,quickSearch):
    if isValid_KeywordCombination(query_1,query_2):
        keyword_1 = db_get_keyword_data(query_1)
        keyword_2 = db_get_keyword_data(query_2)
        if (keyword_combination.objects.filter(keyword_1=keyword_1, keyword_2=keyword_2).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_1,keyword_2=keyword_2)
        elif (keyword_combination.objects.filter(keyword_1=keyword_2, keyword_2=keyword_1).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_2, keyword_2=keyword_1)
        if (result.quick_search_data != quickSearch):
            return False
        else:
            return result
    else:
        return False

def isValid_KeywordCombination(query_1,query_2):
    if (isinDB_KeywordCombination(query_1,query_2)):
        if (isUpdated_KeywordCombination(query_1,query_2)):
            return True
    return False

def store_KeywordCombination(query_1, query_2, average_reader_count, total_publication, growth,quickSearch):
    if isinDB_KeywordCombination(query_1,query_2):
        combination_result = select_KeywordCombination(query_1, query_2, quickSearch)
        if ((isUpdated_KeywordCombination(query_1,query_2)==False) or (combination_result.quick_search_data!=quickSearch)):
            update_KeywordCombination(query_1,query_2,average_reader_count,total_publication,growth,quickSearch)
    else:
        insert_KeywordCombination(query_1, query_2, average_reader_count, total_publication, growth,quickSearch)

# get data from database
def db_select_KeywordCombination(query_1,query_2):
    if isValid_KeywordCombination(query_1,query_2):
        keyword_1 = db_get_keyword_data(query_1)
        keyword_2 = db_get_keyword_data(query_2)
        if (keyword_combination.objects.filter(keyword_1=keyword_1, keyword_2=keyword_2).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_1,keyword_2=keyword_2)
        elif (keyword_combination.objects.filter(keyword_1=keyword_2, keyword_2=keyword_1).exists()):
            result = keyword_combination.objects.get(keyword_1=keyword_2, keyword_2=keyword_1)
        return result
    else:
        return False