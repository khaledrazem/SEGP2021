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
                this_trend = selectSubcat(x)   # get data from db
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
                this_trend = trenddata[x].sum()      # total trend of current week
            else:
                this_trend = 0       # no trend
            
            if status == 1:
                updateSubcat(x, this_trend)    # update db
            else:
                insertSubcat(x, this_trend)    # insert to db
            
            fake.clear()


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
            print(count)
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

# score s1
def s1(scoreDict):
    queryCount = len( scoreDict['singleTopics'] )
    totalTopics = len( scoreDict['allTopics'] )
    s1List = []
    #totalScores includes growth and reader score
    totalScores = 0
    i = 0
    while i < totalTopics:
        if i < queryCount:
            totalScores += scoreDict['growth'][i] + scoreDict['marks'][i]
        else:
            s1List.append( round( scoreDict['growth'][i]*scoreDict['marks'][i] + totalScores, 2) )
        i+=1
    return s1List
# score s2
def s2(scoreDict):
    queryCount = len(scoreDict['singleTopics'])
    s2List = []
    totalPubScore = 0
    i = 0
    for x in scoreDict['marks']:
        if i < queryCount:
            totalPubScore += x
            i += 1
        else:
            s2List.append( round(x + totalPubScore, 2) )
    return s2List
# score s3
def s3(scoreDict):
    queryCount = len(scoreDict['singleTopics'])
    s3List = []
    totalGrowth = 0
    i = 0
    for x in scoreDict['growth']:
        if i < queryCount:
            totalGrowth += x
            i += 1
        else:
            s3List.append( round( x + totalGrowth, 2) )
    return s3List