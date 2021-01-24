from subcategory.db_subcategory_query import *
from subcategory.models import Subcategory
from combinations.db_combination_query import *
from combinations.models import Combination
from pytrends.request import TrendReq
from .mendeleyScores import *
import time

def getTrend(subcat):
    start = time.time()
    trend = []
    topsubcat = []

    for x in subcat:
        if isinSubcatDB(x):
            if isSubcatUpdated(x):
                status = 2
            else:
                status = 1
        else:
            status = 0

        if status < 2:
            fake = []
            fake.append(x)
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = fake
            pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')
            trenddata = pytrends.interest_over_time()
            if not trenddata.empty:
                score = trenddata[x].sum()
            else:
                score = 0
            # print(score)
            if status == 1:
                updateSubcat(x, round(score, 2))
            else:
                insertSubcat(x, round(score, 2))
            fake.clear()

        result = Subcategory.objects.get(name=x)
        this_trend = result.trend_score
        trend.append(this_trend)

    N = 5
    i = 0
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

        if isinCombDB(x):
            if isCombUpdated(x):
                status = 2
            else:
                status = 1
        else:
            status = 0

        if status < 2:
            pages = session.catalog.advanced_search(source=x, view="stats")
            search_result = pages.list(page_size=5).items

            for result in search_result:
                reader += result.reader_count
                count += 1
            avgreader = reader / count

            if status == 1:
                updateComb(x, round(avgreader, 2))
            else:
                insertComb(x, round(avgreader, 2))

        select = Combination.objects.get(name=x)
        this_reader = select.combination_score
        readerCount.append(this_reader)

    largest = sorted(range(len(readerCount)), key=lambda sub: readerCount[sub])[-N:]

    print()
    print("top", N, "combinations")

    while i < len(largest):
        results['topReader'].append(subset[largest[i]])
        results['topComb'].append(readerCount[largest[i]])
        print(subset[largest[i]], "=", readerCount[largest[i]])
        i += 1

    print()

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