from .mendeleyScript import *
from search_keyword.models import Keyword
from .storeData import *

#check if paper is legal
def isLegalType(pageType):
    legalTypes = ["journal", "book", "generic", "book_section", "working_paper", "thesis"]
    for x in legalTypes:
        if(x == pageType):
            return 1
    return 0

#return paired tuples
def pair_subset(query):
    subset = []
    i=0
    while i < len(query):
        j = i+1
        while j < len(query):
            subset.append( ( query[i], query[j] ) )
            j+=1
        i+=1
    return subset
    
#return paired tuples and single queries
def all_subset(query):
    subset = query
    subset += pair_subset(query)
    return subset

#calculate and return growth
def calcAvgGrowth(years):
    i = len(years) - 2
    totalGrowth=0
    while i >= 0:
        totalGrowth += (((years[i]+1)-(years[i+1]+1)) /(years[i+1]+1))
        i -= 1
    avgGrowth = round(totalGrowth / (len(years)-1), 2)
    return avgGrowth

# calculate and return growth and average publication scores
def scoresList(queryList, fromYear):
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
    #calculate scores for all queries
    for query in results['allTopics']:
        if (isinstance(query,str)):
            if  (isValid(query.title())):
                db_result = Keyword.objects.get(name=query.title())
                keyword_result = {
                    'num_of_publication': db_result.total_publication,
                    'average_reader_count': round(db_result.average_reader_count,2),
                    'query_marks': round(round(db_result.average_reader_count,2)/db_result.total_publication, 2),
                    'query_growth': db_result.growth,
                }
            else:
                keyword_result = search(query,fromYear)
            new_data = Keyword(name=query.title(), total_publication=keyword_result['num_of_publication'], average_reader_count=keyword_result['average_reader_count'],
                               score=keyword_result['query_marks'], growth=keyword_result['query_growth'])
            store(new_data)
        else:
            keyword_result = search(query, fromYear)
        results['totalPub'].append(keyword_result['num_of_publication'])
        results['avgReaderC'].append(keyword_result['average_reader_count'])
        results['marks'].append(keyword_result['query_marks'])
        results['growth'].append(keyword_result['query_growth'])
    #zip results
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
            s1List.append( round( scoreDict['growth'][i] * scoreDict['marks'][i] + totalScores, 2) )
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

def search(query,fromYear):

    session = mendeleyAuth()
    curryear = current_year()
    avgReaderPerYear = 0
    pubCount = 0
    pages = session.catalog.advanced_search(source=query, min_year=getStartYear(fromYear), max_year=getEndYear(),
                                            view="stats")
    # initialise new years list
    i = 0
    years = [None] * (fromYear + 1)  # contains all number of publications for all the years
    while i <= fromYear:
        years[i] = 0
        i += 1
    for page in pages.iter(page_size=100):
        if isLegalType(page.type):
            pubCount += 1
            # calculate average reader count per year
            if page.reader_count != None and page.reader_count > 0:
                avgReaderPerYear += page.reader_count / (curryear - page.year)
            years[(current_year() - 1) - page.year] += 1

    query_result = {
        'num_of_publication': pubCount,
        # average reader count per topic
        'average_reader_count': round(avgReaderPerYear, 2),
        # average reader per year per publication
        'query_marks': round(avgReaderPerYear / pubCount, 2),
        # calculate average year of publications
        'query_growth': calcAvgGrowth(years),
    }
    return query_result
