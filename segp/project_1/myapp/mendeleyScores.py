from .mendeleyScript import *
from search_keyword.models import Keyword
from search_keyword.db_keyword_query import *
from combinations.db_keyword_combination import *
from paper.db_paper import *
from paper.db_paper_keyword import *
from combinations.models import keyword_combination
from itertools import combinations
import os

# check if paper is legal
def isLegalType(page):
    legalTypes = ["journal", "book", "generic", "book_section", "working_paper", "thesis"]
    for x in legalTypes:
        if (x == page.type):
            return 1
    return 0

# return paired tuples
def pair_subset(query):
    subset = []
    comb = combinations(query,2)
    for i in comb:
        subset.append(i)
    
    return subset

# return paired tuples and single queries
def all_subset(query):
    subset = query
    subset += pair_subset(query)
    return subset

# calculate and return growth
def calcAvgGrowth(years):
    i = len(years) - 2
    totalGrowth = 0
    while i >= 0:
        totalGrowth += (((years[i] + 1) - (years[i + 1] + 1)) / (years[i + 1] + 1))
        i -= 1
    avgGrowth = round(totalGrowth / (len(years) - 1), 2)
    return avgGrowth

# calculate and return growth and average publication scores
def scoresList(queryList, quickSearch):
    os.system('cls')
    # dictionary containing lists needed to be returned
    results = {
        'singleTopics': queryList,
        'combTopics': pair_subset(queryList),
        'allTopics': all_subset(queryList),
        # total publications
        'totalPub': [],
        # average reader count per topic
        'avgReaderC': [],
        # average reader per year per publication
        'marks': [],
        # growth score of topics
        'growth': [],
        'zipped': []
    }
    # calculate scores for all queries
    for query in results['allTopics']:
        if (isinstance(query, str)):
            db_result = get_keyword_data(query.title(),quickSearch)
            if (db_result != False):
                keyword_result = {
                    'num_of_publication': db_result.total_publication,
                    'average_reader_count': db_result.average_reader_count,
                    'query_marks': db_result.score,
                    'query_growth': db_result.growth,
                    'query_paper': []
                }
            else:
                keyword_result = search(query, quickSearch)
            new_data = Keyword(name=query.title(), total_publication=keyword_result['num_of_publication'],
                               average_reader_count=keyword_result['average_reader_count'],
                               score=keyword_result['query_marks'], growth=keyword_result['query_growth'], quick_search_data=quickSearch)
            storeKeyword(new_data)
        elif (isinstance(query, tuple)):
            db_comb_result = select_KeywordCombination(query[0].title(), query[1].title(), quickSearch)
            if (db_comb_result != False):
                keyword_result = {
                    'num_of_publication': db_comb_result.total_publication,
                    'average_reader_count': db_comb_result.average_reader_count,
                    'query_marks': db_comb_result.score,
                    'query_growth': db_comb_result.growth,
                    'query_paper': []
                }
            else:
                keyword_result = search(query, quickSearch)
            store_KeywordCombination(query_1=query[0].title(), query_2=query[1].title(), average_reader_count=keyword_result['average_reader_count'], total_publication=keyword_result['num_of_publication'], growth=keyword_result['query_growth'], quickSearch=quickSearch)
        for i in keyword_result['query_paper']:
            store_Paper(paper_title=i[2], paper_reader_count=i[0], paper_link=i[1], paper_year_published=i[3])
            if (isinstance(query, str)):
                store_Paper_keyword(paper_title=i[2], keyword_1=query, keyword_2=None)
            elif (isinstance(query, tuple)):
                store_Paper_keyword(paper_title=i[2], keyword_1=query[0].title(), keyword_2=query[1].title())
        results['totalPub'].append(keyword_result['num_of_publication'])
        results['avgReaderC'].append(keyword_result['average_reader_count'])
        results['marks'].append(keyword_result['query_marks'])
        results['growth'].append(keyword_result['query_growth'])
    # zip results
    all_query=[]
    for i in results['singleTopics']:
        if isinstance(i,str):
            i=(i.title(),'-')
        else:
            i=(i[0].title,i[1].title)
        all_query.append(i)
    results['singleTopics']=all_query
    results['zipped'] = zip(results['singleTopics'], results['marks'])

    return results

def search(query, quickSearch):
    fromYear = 5
    session = mendeleyAuth()
    curryear = current_year()
    avgReaderPerYear = 0
    pubCount = 0
    searchNum = 0
    popular_article_list=[]
    pages = session.catalog.advanced_search(title=query, min_year=getStartYear(fromYear), max_year=getEndYear(),
                                            view="stats")
    # initialise new years list
    i = 0
    years = [None] * (fromYear + 1)  # contains all number of publications for all the years
    while i <= fromYear:
        years[i] = 0
        i += 1
    for page in pages.iter(page_size=100):
        if isLegalType(page):
            pubCount += 1
            popular_article_list = popular_article(popular_article_list,page.reader_count,page.link,page.title,page.year)
            # calculate average reader count per year
            if page.reader_count != None and page.reader_count > 0:
                avgReaderPerYear += page.reader_count / (curryear - page.year)
            years[(current_year() - 1) - page.year] += 1
        if quickSearch:
            if searchNum >= 100:  # limited to 100 serach results
                break
        searchNum += 1
    query_result = {
        'num_of_publication': pubCount,
        # average reader count per topic
        'average_reader_count': round(avgReaderPerYear, 2),
        # average reader per year per publication
        'query_marks': round((avgReaderPerYear+1) / (pubCount+1), 2),
        # calculate average year of publications
        'query_growth': calcAvgGrowth(years),
        'query_paper': popular_article_list,
    }
    return query_result

def popular_article(list_of_link,reader_count,link,title,year_published):
    if len(list_of_link) < 5:
        new_data = (reader_count,link,title,year_published)
        list_of_link.append(new_data)
    else:
        if reader_count != None:
            for (w, x, y, z) in list_of_link:
                if reader_count > w:
                    list_of_link.remove((w, x, y, z))
                    new_data = (reader_count, link,title, year_published)
                    list_of_link.append(new_data)
                    break
    return list_of_link
