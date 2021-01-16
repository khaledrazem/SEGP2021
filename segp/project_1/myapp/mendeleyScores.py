from myapp.mendeleyScript import *

#check if paper is legal
def isLegalType(pageType):
    legalTypes = [ "journal", "book", "generic", "book_section", "working_paper", "thesis"]
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
        totalGrowth += ((years[i]-years[i+1]) /years[i+1])
        i -= 1
    avgGrowth = round(totalGrowth / (len(years)-1), 2)
    return avgGrowth

# calculate and return growth and average publication scores
def scoresList(queryList, fromYear):
    session = mendeleyAuth()
    curryear = current_year()
    #dictionary containing lists needed to be returned
    results = {
        'singleTopics':[],
        'combTopics':[],
        'allTopics':[],
        #total publications
        'totalPub':[],
        #average reader count per topic
        'avgReaderC':[],
        #average reader per year per publication
        'marks':[],
        # growth score of topics
        'growth':[],
        'zipped':[]
    }
    results['singleTopics'] += queryList 
    results['combTopics'] += pair_subset(queryList) 
    results['allTopics'] += all_subset(queryList)
    #calculate scores for all queries
    for query in results['allTopics']:
        pages = session.catalog.advanced_search(source=query, min_year=getStartYear(fromYear), max_year=getEndYear(), view="stats" )
        #initialise new years list
        i = 0
        years = [None] * (fromYear+1) #contains all number of publications for all the years
        while i <= fromYear:
            years[i] = 0
            i+=1
        avgReaderPerYear = 0
        pubCount = 0
        for page in pages.iter(page_size=100):
            if isLegalType(page.type):
                pubCount += 1
        #calculate average reader count per year
                if page.reader_count != None and page.reader_count > 0 :
                    avgReaderPerYear += page.reader_count / (curryear - page.year)
                years[ (getCurrYear()-1)-page.year ] +=1
        #calculate average year of publications
        results['totalPub'].append( pubCount )
        results['avgReaderC'].append(round(avgReaderPerYear))
        results['marks'].append(round( avgReaderPerYear / pubCount ,2))
        results['growth'].append(calcAvgGrowth(years))
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


# for debugging only ( remove during implementation )
def getDemoList(queryList):
    results = {
        'singleTopics':[],
        'combTopics':[],
        'allTopics':[],
        'totalPub': [2057, 6769, 1321, 2913, 2276, 7069],
        'avgReaderC': [111032, 145621, 10684, 130547, 106926, 150538],
        'marks': [53.98, 21.51, 8.09, 44.82, 46.98, 21.3],
        'growth': [-0.23, -0.17, -0.02, -0.16, -0.23, -0.18]
    }
    results['singleTopics'] += queryList
    results['combTopics'] += pair_subset(queryList)
    results['allTopics'] += all_subset(queryList)
    return results

# debugging (remove during implementation)
def main():
    import time
    l = [ "computer vision", "neural networks", "algae neurons" ]

    start_time = time.time()
    result = scoresList(l, 5)
    print("\n execution time: %s seconds \n" % (time.time() - start_time))

    print("--------------------------\n Scores: \n--------------------------")
    print( s1(result) )
    print( s2(result) )
    print( s3(result) )

    #print contents of dictionary
    print("--------------------------\n Dictionary: \n--------------------------")
    for key, val in result.items():
        print( key, end=": ")
        print( val )
    print("\n")

if __name__ == "__main__":
    main();