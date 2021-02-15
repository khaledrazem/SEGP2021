from .mendeleyScores import *
from .author import *
from pytrends.request import TrendReq
from subcategory.db_subcategory_query import *
from combinations.db_subcategory_combination import *
from paper.db_paper import *
from paper.db_paper_subcategory import *
from .elsevier_test import *
import time

def getTrend(subcat,quick,growth_query,authorscore_query,readercount_query):
    start = time.time()
    trend = []
    topsubcat = []

    print()
    for x in subcat:

        # check status of data
        if isinSubcatDB(x):
            subcat_result = selectSubcat(x)
            if (isSubcatUpdated(x)==False) or subcat_result.quick_search_data!=quick:
                status = 1  # in db but not updated
            else:
                status = 2  # in db and is updated
                this_trend = subcat_result.trend_score
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
                this_trend = float(trenddata[x].sum())      # total trend of current week
            else:
                this_trend = 0       # no trend

            if status == 1:
                updateSubcat(x, this_trend, quick)    # update db
            else:
                insertSubcat(x, this_trend, quick)    # insert to db

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
        'realresult': topCombination(combinations,quick,growth_query,authorscore_query,readercount_query)
    }

    end = time.time()
    print("total time used:", end - start, "s")
    print()

    return results
    # pair_subset(topsubcat,start)


def topCombination(subset,quick,growth_query,authorscore_query,readercount_query):
    session = mendeleyAuth()
    readerCount = []
    authorScore = []
    Growth = []
    results = {
        'topReader': [],
        'topComb': [],
        'zipped': []
    }
    i = 0
    N = 10

    for x in subset:
        popular_article_list=[]
        reader = count = avgreader = this = 0
        # check status of data
        if isinCombDB(query_1=x[0],query_2=x[1]):
            print(x[0],"and",x[1],"in comb db")
            comb_result = selectComb(query_1=x[0],query_2=x[1])
            if (isCombUpdated(query_1=x[0],query_2=x[1])==False) or (comb_result.quick_search_data != quick):
                status = 1      # in db but not updated
            else:
                status = 2      # in db and is updated
        else:
            status = 0      # not in db

        if status < 2:
            pages = session.catalog.advanced_search(title=x, view="stats")
            authorList=[]
            
            a = 0
            fromYear=500
            years = [None] * (fromYear + 1)  # contains all number of publications for all the years
            while a <= fromYear:
                years[a] = 0
                a += 1
            
            for page in pages.iter(page_size=100):
                reader += page.reader_count
                count += 1
                
                repeat = 0
                author = page.authors
                authorscore = 0
                if author != None:
                    for authorName in author:
                        if authorName.last_name != None:
                            last_name = authorName.last_name
                        else:
                            last_name = ""
                        if authorName.first_name != None:
                            first_name = authorName.first_name
                        else:
                            first_name = ""
                        name = first_name + " " + last_name
                        #sprint(name)

                        for y in authorList:
                            if y == name:
                                repeat += 1
                                continue
                        if repeat == 0:     
                            authorList.append(name)
                            #print(name)
                            #print("==========================================================================================================")
                           
                
                popular_article_list = popular_article(popular_article_list, page.reader_count, page.link, page.title,
                                                       page.year)
                
                if page.year == None:
                    page.year = current_year()
                
                index=(current_year() - 1) - page.year
                
                years[index] += 1
                growth=calcAvgGrowth(years)
                
                
                if quick:
                    if count >= 100:
                        break
            
            
            #for x in authorList:            
            #    authorScore+=author_score(x)

            
            avgreader = round((reader+1) / (count+1),2)
            for i in popular_article_list:
                store_Paper(paper_title=i[2], paper_reader_count=i[0], paper_link=i[1], paper_year_published=i[3])
                store_Paper_subcategory(paper_title=i[2], query_1=x[0].title(), query_2=x[1].title())
            
            #authorscore = author_score(authorList)

            if status == 1:
                updateComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=round(authorscore, 2), growth=round(growth, 2), quickScore=quick)  # update db
            else:
                insertComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=round(authorscore, 2), growth=round(growth, 2), quickScore=quick)  # insert to db
                

        if status == 2:
            comb_result = selectComb(query_1=x[0], query_2=x[1])    # get data from db
            readerCount.append(comb_result.combination_score)
            authorScore.append(comb_result.combination_authorscore)
            Growth.append(comb_result.combination_growth)
        else:
            readerCount.append(avgreader)       # get data from calc
            authorScore.append(str(authorscore))
            Growth.append(str(growth))

    #print(readerCount)
    
    score = []
    if readercount_query and growth_query and authorscore_query:
        score = readerCount
    else:
        if readercount_query and growth_query:
            zipped_lists = zip(readerCount, Growth)
            score = [float(x) + float(y) for (x, y) in zipped_lists]
        elif readercount_query and authorscore_query:
            zipped_lists = zip(readerCount, authorScore)
            score = [float(x) + float(y) for (x, y) in zipped_lists]
        elif growth_query and authorscore_query:
            zipped_lists = zip(authorScore, Growth)
            score = [float(x) + float(y) for (x, y) in zipped_lists]
        elif readercount_query:
            score = readerCount
        elif growth_query:
            score = Growth
        elif authorscore_query: 
            score = authorScore
        else:
            score = readerCount
    
    # get position of largest data
    largest = sorted(range(len(score)), key=lambda sub: score[sub])[-N:]

    print()
    print("top", N, "combinations")

    # store data into dictionary
    z=0
    while z < len(largest):
        results['topReader'].append(subset[largest[z]])
        results['topComb'].append(score[largest[z]])
        print(subset[largest[z]], "=", score[largest[z]])
        z += 1

    print()

    results['topReader'].reverse()
    results['topComb'].reverse()
    results['zipped'] = zip(results['topReader'], results['topComb'])

    return results

def filterSubcat(q1,q2,op,score,quick):

    results = {
        'realresult': filterResult(q1,q2,op,score,quick)
    }
    
    return results

def filterResult(q1,q2,op,score,quick):
    subcat = q1 + q2
    
    session = mendeleyAuth()
    readerCount = []
    results = {
        'topReader': [],
        'realReader': [],
        'topComb': [],
        'realComb': [],
        'zipped': []
    }
    
    readers=[]
    comb=[]
    i = 0
    
    subset = pair_subset(subcat)

    for x in subset:
        popular_article_list=[]
        reader = count = avgreader = this = 0
        # check status of data
        if isinCombDB(query_1=x[0],query_2=x[1]):
            comb_result = selectComb(query_1=x[0],query_2=x[1])
            if (isCombUpdated(query_1=x[0],query_2=x[1])==False) or (comb_result.quick_search_data != quick):
                status = 1      # in db but not updated
            else:
                status = 2      # in db and is updated
        else:
            status = 0      # not in db

        if status < 2:
            pages = session.catalog.advanced_search(title=x, view="stats")
            
            a = 0
            fromYear=500
            years = [None] * (fromYear + 1)  # contains all number of publications for all the years
            while a <= fromYear:
                years[a] = 0
                a += 1

            for page in pages.iter(page_size=100):
                reader += page.reader_count
                count += 1
                popular_article_list = popular_article(popular_article_list, page.reader_count, page.link, page.title,page.year)
                
                years[(current_year() - 1) - page.year] += 1
                growth=calcAvgGrowth(years)
                
                if quick:
                    if count >= 100:
                        break
            
            avgreader = round((reader+1) / (count+1),2)
            for i in popular_article_list:
                store_Paper(paper_title=i[2], paper_reader_count=i[0], paper_link=i[1], paper_year_published=i[3])
                store_Paper_subcategory(paper_title=i[2], query_1=x[0], query_2=x[1])
            authorscore = 0
            
            if status == 1:
                updateComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=round(authorscore, 2), growth=round(growth, 2), quickScore=quick)  # update db
            else:
                insertComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=round(authorscore, 2), growth=round(growth, 2), quickScore=quick)  # insert to db


        if status == 2:
            comb_result = selectComb(query_1=x[0], query_2=x[1])    # get data from db
            readerCount.append(comb_result.combination_score)
        else:
            readerCount.append(avgreader)       # get data from calc

    print(readerCount)
    
    N=len(readerCount)

    # get position of largest data
    largest = sorted(range(len(readerCount)), key=lambda sub: readerCount[sub])[-N:]

    print()
    print("top", N, "combinations")

    # store data into dictionary
    z=0
    while z < len(largest):
        #results['topReader'].append(subset[largest[z]])
        #results['topComb'].append(readerCount[largest[z]])
        
        
        readers.append(subset[largest[z]])
        comb.append(readerCount[largest[z]])
        
        print(subset[largest[z]], "=", readerCount[largest[z]])
        z += 1

    print()

    #results['topReader'].reverse()
    #results['topComb'].reverse()
    
    
    readers.reverse()
    comb.reverse()
    
    if score == '':
        score = 0
    
    if not op or len(op) == 3:
        results['realReader'] = readers
        results['realComb'] = comb
        
    elif len(op) == 2:
        if op[0] == 'greater':
            if op[1] == 'smaller':      #><
                m = [pos for pos, val in enumerate(comb) if val == float(score)]
                if m:
                    first=m[0]
                    last=m[len(m)-1]
                    del readers[first:last]
                    del comb[first:last]
                results['realReader'] = readers
                results['realComb'] = comb
            else:                       #>=
                try:
                    m = next(pos for pos, val in enumerate(comb) if val < float(score))
                    results['realReader'] = readers[:m]
                    results['realComb'] = comb[:m]
                except:
                    results['realReader'] = readers
                    results['realComb'] = comb
            
        elif op[0] == 'smaller':
            if op[1] == 'greater':      #<>
                m = [pos for pos, val in enumerate(comb) if val == float(score)]
                if m:
                    first=m[0]
                    last=m[len(m)-1]
                    del readers[first:last]
                    del comb[first:last]
                results['realReader'] = readers
                results['realComb'] = comb
            else:                       #<=
                try:
                    m = next(pos for pos, val in enumerate(comb) if val <= float(score))
                    results['realReader'] = readers[m:]
                    results['realComb'] = comb[m:]
                except:
                    results['realReader'] = readers
                    results['realComb'] = comb
        
    else:
        if op[0] == 'greater':
            try:
                m = next(pos for pos, val in enumerate(comb) if val <= float(score))
                results['realReader'] = readers[:m]
                results['realComb'] = comb[:m]
            except:
                results['realReader'] = readers
                results['realComb'] = comb
            
        elif op[0] == 'smaller':
            try:
                m = next(pos for pos, val in enumerate(comb) if val < float(score))
                results['realReader'] = readers[m:]
                results['realComb'] = comb[m:]
            except:
                results['realReader'] = readers
                results['realComb'] = comb
        
        else:
            m = [pos for pos, val in enumerate(comb) if val == float(score)]
            if m:
                q = 0
                while q < len(m):
                    results['realReader'].append(readers[m[q]])
                    results['realComb'].append(comb[m[q]])
                    q += 1
            else:
                results['realReader'] = readers
                results['realComb'] = comb
        
    results['zipped'] = zip(results['realReader'], results['realComb'])

    return results

"""
def author_score(queryList):
    count=0
    session = mendeleyAuth()
    author_name=' \"' +queryList+ '\"'
    oter=session.catalog.advanced_search(author=author_name,view='all')
    for otr in oter.iter(page_size=100):
        print(otr.id)
        count+=1
    return count
"""








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