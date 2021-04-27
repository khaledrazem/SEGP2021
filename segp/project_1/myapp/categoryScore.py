# file created by group
# mendeley and elsevier is created with reference from mendeley and elsevier documentations

from .mendeleyScores import *
from pytrends.request import TrendReq
from topic.db_topic_query import *
from combinations.db_topic_combination import *
from paper.db_paper import *
from paper.db_paper_topic import *
from .elsevier_test import *
from .async_search import *
import time
import os

def getTrend(topic,code):
    os.system('cls')
    start = time.time()
    trend = []
    toptopic = []
    print()
    for x in topic:
        # check status of data
        status = checkTopicStatus(x)
        
        if status < 2:
            connection = this_trend = 0
            
            # check current trend of the keyword
            pytrends = TrendReq(hl='en-US', tz=360)
            kw_list = []
            kw_list.append(x)
            pytrends.build_payload(kw_list, cat=0, timeframe='now 7-d', geo='', gprop='')
                
            try:
                trenddata = pytrends.interest_over_time()
                connection = 1
            except:
                print("Unable to connect to Google Trends! Try Again Later!")
            
            # connected to google trend and have data
            if connection == 1: 
                if not trenddata.empty:
                    # total trend of current week
                    this_trend = float(trenddata[x].sum())      
                    
            if status == 1 and connection == 1:
                # update db
                updateTopic(x, this_trend)    
            elif status == 0:
                # insert to db
                insertTopic(x, this_trend)    

        # get data from db
        topic_result = selectTopic(x)
        this_trend = topic_result.trend_score
        trend.append(this_trend)
    
    # set top n keywords
    if len(trend) > 6:
        N = 6
    else:
        N = len(trend)
    
    # get position of largest n data
    largest = sorted(range(len(trend)), key=lambda sub: trend[sub])[-N:]
    
    # get top N subcategory
    print()
    print("top", N, "subcategory")
    i = 0
    while i < len(largest):
        print(topic[largest[i]], "=", trend[largest[i]])
        toptopic.append(topic[largest[i]])
        i += 1
    print()

    # pair subsets
    combinations = pair_subset(toptopic)
    
    results = {
        'realresult': topCombination(combinations,code),
    }

    end = time.time()
    print("total time used:", end - start, "s")
    print()

    return results

def topCombination(topic,code):
    session = mendeleyAuth()
    client = elsevier_auth()
    readerCount = []
    authorScore = []
    Growth = []
    pieScore = []
    results = {
        'topReader': [],
        'topComb': [],
        'zipped': [],
    }

    for x in topic:
        # check status of data
        status = checkCombStatus(x)

        if status < 2:
            # search data
            searchData(x,client,session,status)
        
        # get data from db
        comb_result = selectComb(query_1=x[0], query_2=x[1])
        readerCount.append(comb_result.combination_score)
        authorScore.append(comb_result.combination_authorscore)
        Growth.append(comb_result.combination_growth)
        pieScore.append(comb_result.combination_pie)
    
    # normalize data
    readerCount = data_norm(readerCount)
    Growth = data_norm(Growth)
    pieScore = data_norm(pieScore)
    authorScore = data_norm(authorScore)
    
    # choose which data to display
    score = chooseDisplayData(code,readerCount,Growth,authorScore,pieScore)
    
    # get position of largest n data
    N = 15
    largest = sorted(range(len(score)), key=lambda sub: score[sub])[-N:]

    print()
    print("Top combinations")
    # store top N combinations data into dictionary
    z=0
    while z < len(largest):
        results['topReader'].append(topic[largest[z]])
        results['topComb'].append(score[largest[z]])
        print(topic[largest[z]], "=", score[largest[z]])
        z += 1
    print()

    # sort descending
    results['topReader'].reverse()
    results['topComb'].reverse()
    results['zipped'] = zip(results['topReader'], results['topComb'])

    return results

def filterResult(q1,q2,minval,maxval,code):
    os.system('cls')
    start = time.time()
    session = mendeleyAuth()
    client = elsevier_auth()
    topics = []
    readerCount = []
    Growth = []
    pieScore = []
    authorScore = []
    readers=[]
    comb=[]
    results = {
        'topReader': [],
        'realReader': [],
        'topComb': [],
        'realComb': [],
        'zipped': [],
    }
    
    # find all subcategory combination
    all_comb = pair_subset(q2)
    
    if not q1:
        # default select all
        topics = all_comb
    else:
        # keep checked subcategory
        for p in all_comb:
            for q in q1:
                if q in p:
                    topics.append(p)
        topics = list(dict.fromkeys(topics))

    for x in topics:
        # check status of data
        status = checkCombStatus(x)
        
        if status < 2:
            # search data
            searchData(x,client,session,status)
        
        # get data from db
        comb_result = selectComb(query_1=x[0], query_2=x[1])    
        readerCount.append(comb_result.combination_score)
        authorScore.append(comb_result.combination_authorscore)
        Growth.append(comb_result.combination_growth)
        pieScore.append(comb_result.combination_pie)

    # normalize data
    readerCount = data_norm(readerCount)
    Growth = data_norm(Growth)
    pieScore = data_norm(pieScore)
    authorScore = data_norm(authorScore)
    
    # choose display data
    score = chooseDisplayData(code,readerCount,Growth,authorScore,pieScore)
    
    # get position of largest n data
    N=len(score)
    largest = sorted(range(len(score)), key=lambda sub: score[sub])[-N:]

    print()
    print("All combinations")
    # store top N combinations into array
    z=0
    while z < len(largest):
        readers.append(topics[largest[z]])
        comb.append(score[largest[z]])
        print(topics[largest[z]], "=", score[largest[z]])
        z += 1
    print()

    # sort descending order
    readers.reverse()
    comb.reverse()
    
    # default min = 0, max = 100
    if minval == '':
        minval = 0
    if maxval == '':
        maxval = 100
     
    # >=
    try:
        m = next(pos for pos, val in enumerate(comb) if val < float(minval))
        readers = readers[:m]
        comb = comb[:m]
    except:
        readers = readers
        comb = comb
    
    # <=
    try:
        m = next(pos for pos, val in enumerate(comb) if val <= float(maxval))
        results['realReader'] = readers[m:]
        results['realComb'] = comb[m:]
    except:
        results['realReader'] = readers
        results['realComb'] = comb
        
    results['zipped'] = zip(results['realReader'], results['realComb'])
    
    actualResult = {
        'realresult': results,
    }
    
    end = time.time()
    print("total time used:", end - start, "s")
    print()
    
    return actualResult

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

def data_norm(arr):
    max_val = float(max(arr)) * 1.05
    min_val = float(min(arr)) * 0.95
    score = []
    
    for x in arr:
        point = (float(x) - min_val)/((max_val - min_val)+1)*100
        if point > 100:
            point = 100
        score.append(round(point,2))
    
    return score

def getCode(readercount_query,growth_query,authorscore_query,pie_query):
    tempcode = [0]*4
    if readercount_query:
        tempcode[0] = 1
    if growth_query:
        tempcode[1] = 1
    if authorscore_query:
        tempcode[2] = 1
    if pie_query:
        tempcode[3] = 1
    
    code = ""
    
    for s in tempcode:
        code += str(s)
    
    return code

def searchData(x,client,session,status):
    reader = count = avgreader = pie_score  = a = growth  = 0
    all_paper = []
    fromYear = 150
    if status != None:
        query = x[0] + " " + x[1]
    else:
        query = x
    this_year = current_year()
    
    # search fom elsevier
    myDocSrch = ElsSearch(query,'sciencedirect')
    myDocSrch.execute(client,get_all = False)
    
    base_url = "https://www.sciencedirect.com/science/article/pii/"
    title = []
    year = []
    link = []
    doi = []
    rc = []
    
    # define year array
    years = [None] * (fromYear + 1) 
    while a <= fromYear:
        years[a] = 0
        a += 1
    min_yr = current_year() - 99
    
    
    for ans in myDocSrch.results:
        yr_pub = int(ans['prism:coverDate'][:4])    # year publish
        
        if yr_pub > min_yr:
            try:
                title.append(ans['dc:title'])   # paper title
                doi.append(ans['prism:doi'])        # paper doi
            except:
                continue
            
            year.append(yr_pub)
            yr_diff = this_year - yr_pub
            link.append(base_url + ans['pii'])  # paper link
            
            # paper reader count
            try:
                temp_rc = session.catalog.by_identifier(doi=ans['prism:doi'], view='stats').reader_count
            except:
                temp_rc = 0
                
            rc.append(temp_rc)
            new_paper = [ans['prism:doi'], temp_rc, yr_diff]
            all_paper.append(new_paper)
            
            years[yr_diff] += 1
            
            count += 1
    
    # get growth score
    growth = calcAvgGrowth(years)
    
    # get reader count score
    totalrc = sum(rc)
    if count == 0: count = 1
    avgreader = round((totalrc / count),2)
	
    # get pie and author score
    the_data = calcData(all_paper)
    authorscore = the_data['author']
    pieScore = the_data['pie']
    
    paper_zip = zip(title, rc, link, year)

    if status != None:
        for a,b,c,d in paper_zip:
            if b > 0:
                # store paper into database
                store_Paper(paper_title=a, paper_reader_count=b, paper_link=c, paper_year_published=d)
                store_Paper_topic(paper_title=a, query_1=x[0], query_2=x[1])
    
        if status == 1:
            # update db
            updateComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=pieScore)
        else:
            # insert to db
            insertComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=pieScore)
    else:
        os.system('cls')
        
        # return data from calculation
        results = {
            'reader': avgreader,
            'author': authorscore,
            'growth': growth,
        }
        return results

def chooseDisplayData(code,readerCount,Growth,authorScore,pieScore):
    temp = [readerCount,Growth,authorScore,pieScore]
    j = 0
    displayData = []
    score = []
    
    if '1' not in code:     # calculate display all scores
        zip_list = zip(readerCount,Growth,authorScore,pieScore)
        
        for a,b,c,d in zip_list:
            score.append(round(((a+b+c+d)/4),2))
    else:
        # add the scores selected
        for i in code:
            if i == '1':
                displayData.append(temp[j])
            j+=1
        
        # calculate the score
        for x in range(len(readerCount)):
            tempscore = 0
            for y in displayData:
                tempscore += float(y[x])
            score.append(round((tempscore/len(displayData)),2))
    
    return score
