from myapp.mendeleyScript import *
from myapp.storeData import *

def all_subset(query):
    from itertools import combinations
    subset = []
    if len(query) > 2:
        for i in set(combinations(query, r=2)):
            subset.append(i)
        for i in set(combinations(query, r=1)):
            subset.append(i)
    else:
        for i in set(combinations(query, r=1)):
            subset.append(i)
    return subset

def avgRCSList(queryList):
    session = mendeleyAuth()
    avgRCS =0
    curryear = current_year() #get the current year
    resultList = []

    queryList_subset = all_subset(queryList)
    for query in queryList_subset:
        x = 0
        iterCount = 0
        paperCount = 0
        avgRCS = 0
        avgyear = 0
        pages = session.catalog.advanced_search(source=query, view="stats")

        for page in pages.iter(page_size=100):
            if iterCount == 1000:
                break
            if curryear - page.year <= 0:
                x += 0
            else:
                x += page.reader_count / (curryear - page.year)
                paperCount += 1
            iterCount += 1
            avgyear += page.year #calculate average year of publications

        avgyear = avgyear / iterCount
        avgRCS = round((x / paperCount),2)
        resultList.append(avgRCS)
        print(str(query) + ": " + str(avgRCS) + " | published: " + str(paperCount) + " | avgyear: " + str(round(avgyear)))
        
        store(query,avgRCS)
        
        results = {

            'subset':queryList_subset,
            'marks':resultList,
            'zipped':zip(queryList_subset,resultList),
        }

    return results
