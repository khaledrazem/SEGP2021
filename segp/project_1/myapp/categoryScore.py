from .mendeleyScores import *
from pytrends.request import TrendReq
from subcategory.models import Subcategory
from combinations.models import Combination
from subcategory.db_subcategory_query import *
from combinations.db_combination_query import *
import time

def getTrend(subcat):
    start = time.time()
    trend = []
    topsubcat = []

    print()
    for x in subcat:
        
        # check status of data
        if isinSubcatDB(x):
            if isSubcatUpdated(x):
                status = 2      #in db and updated
            else:
                status = 1      #in db but not updated
        else:
            status = 0      #not in db

        
        if status < 2:
            # check current trend of the keyword
            fake = []
            fake.append(x)
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = fake
            pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')
            trenddata = pytrends.interest_over_time()
            
            if not trenddata.empty:
                score = trenddata[x].sum()      # total trend of current week
            else:
                score = 0       # no trend
            
            if status == 1:
                updateSubcat(x, score)    # update db
            else:
                insertSubcat(x, score)    # insert to db
            
            fake.clear()

        # get data from db
        this_trend = selectSubcat(x)
        trend.append(this_trend)

    N = 5
    i = 0
    
    # get position of largest data
    largest = sorted(range(len(trend)), key=lambda sub: trend[sub])[-N:]

    print()
    print("top", N, "subcategory")
    
    while i < len(largest):
        print(subcat[largest[i]], "=", trend[largest[i]])
        topsubcat.append(subcat[largest[i]])
        i += 1
    
    print()
    
    combinations = pair_subset(topsubcat)

    results = {
        'realresult': topCombination(combinations)
    }

    end = time.time()
    print("total time used:", end - start, "s")
    print()
    
    return results
    # pair_subset(topsubcat,start)


def topCombination(subset):
    session = mendeleyAuth()
    readerCount = []
    results = {
        'topReader': [],
        'topComb': [],
        'zipped': []
    }
    
    i = 0
    N = 10

    for x in subset:
        reader = count = avgreader = this = 0
        
        # check status of data
        if isinCombDB(x):
            if isCombUpdated(x):
                status = 2      # in db and updated
            else:
                status = 1      # in db but not updated
        else:
            status = 0      # not in db

        if status < 2:
            pages = session.catalog.advanced_search(source=x, view="stats")
            search_result = pages.list(page_size=5).items
            
            # get avg reader count
            for result in search_result:
                reader += result.reader_count
                count += 1
            avgreader = reader / count

            if status == 1:
                updateComb(x, round(avgreader, 2))  # update db
            else:
                insertComb(x, round(avgreader, 2))  # insert to db
        
        # get data from db
        this_reader = selectComb(x)
        readerCount.append(this_reader)
    
    # get position of largest data
    largest = sorted(range(len(readerCount)), key=lambda sub: readerCount[sub])[-N:]

    print()
    print("top", N, "combinations")

    # store data into dictionary
    while i < len(largest):
        results['topReader'].append(subset[largest[i]])
        results['topComb'].append(readerCount[largest[i]])
        print(subset[largest[i]], "=", readerCount[largest[i]])
        i += 1

    print()
    
    results['topReader'].reverse()
    results['topComb'].reverse()
    
    results['zipped'] = zip(results['topReader'], results['topComb'])

    return results


def catScoresList(queryList, fromYear):
    results = {
        'singleTopics': queryList,
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

    for query in results['singleTopics']:
        if (isinstance(query, str)):
            if (isValid(query.title())):
                db_result = Keyword.objects.get(name=query.title())
                keyword_result = {
                    'num_of_publication': db_result.total_publication,
                    'average_reader_count': round(db_result.average_reader_count, 2),
                    'query_marks': round(round(db_result.average_reader_count, 2) / db_result.total_publication, 2),
                    'query_growth': db_result.growth,
                }
            else:
                keyword_result = search(query, fromYear)
            new_data = Keyword(name=query.title(), total_publication=keyword_result['num_of_publication'],
                               average_reader_count=keyword_result['average_reader_count'],
                               score=keyword_result['query_marks'], growth=keyword_result['query_growth'])
            store(new_data)
        else:
            keyword_result = search(query, fromYear)
        results['totalPub'].append(keyword_result['num_of_publication'])
        results['avgReaderC'].append(keyword_result['average_reader_count'])
        results['marks'].append(keyword_result['query_marks'])
        results['growth'].append(keyword_result['query_growth'])

    results['zipped'] = zip(results['singleTopics'], results['marks'])

    return results