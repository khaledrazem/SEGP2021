from .mendeleyScores import *
from .author import *
from pytrends.request import TrendReq
from subcategory.db_subcategory_query import *
from combinations.db_subcategory_combination import *
from paper.db_paper import *
from paper.db_paper_subcategory import *
from .elsevier_test import *
from .async_search import *
import time
import os

def getTrend(subcat,quick,code):
    os.system('cls')
    start = time.time()
    trend = []
    topsubcat = []
    
    print()
    for x in subcat:
        # check status of data
        status = checkSubcatStatus(x)
        
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
                updateSubcat(x, this_trend)    
            elif status == 0:
                # insert to db
                insertSubcat(x, this_trend)    

        # get data from db
        subcat_result = selectSubcat(x)
        this_trend = subcat_result.trend_score
        trend.append(this_trend)
    
    if len(trend) > 5:
        N = 5
    else:
        N = len(trend)
    
    # get position of largest n data
    largest = sorted(range(len(trend)), key=lambda sub: trend[sub])[-N:]
    
    # get top N subcategory
    print()
    print("top", N, "subcategory")
    i = 0
    while i < len(largest):
        print(subcat[largest[i]], "=", trend[largest[i]])
        topsubcat.append(subcat[largest[i]])
        i += 1
    print()

    combinations = pair_subset(topsubcat)
    
    results = {
        'realresult': topCombination(combinations,quick,code),
    }

    end = time.time()
    print("total time used:", end - start, "s")
    print()

    return results

def topCombination(subset,quick,code):
    session = mendeleyAuth()
    readerCount = []
    authorScore = []
    Growth = []
    pieScore = []
    results = {
        'topReader': [],
        'topComb': [],
        'zipped': [],
    }

    for x in subset:
        # check status of data
        status = checkCombStatus(x,quick)

        if status < 2:
            # search data
            searchData(x,session,status,quick)
        
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
    N = 10
    largest = sorted(range(len(score)), key=lambda sub: score[sub])[-N:]

    print()
    print("top", N, "combinations")
    # store top N combinations data into dictionary
    z=0
    while z < len(largest):
        results['topReader'].append(subset[largest[z]])
        results['topComb'].append(score[largest[z]])
        print(subset[largest[z]], "=", score[largest[z]])
        z += 1
    print()

    # sort descending
    results['topReader'].reverse()
    results['topComb'].reverse()
    results['zipped'] = zip(results['topReader'], results['topComb'])

    return results

def filterResult(q1,q2,minval,maxval,code,quick):
    os.system('cls')
    start = time.time()
    session = mendeleyAuth()
    subset = []
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
        subset = all_comb
    else:
        # keep checked subcategory
        for p in all_comb:
            for q in q1:
                if q in p:
                    subset.append(p)
        subset = list(dict.fromkeys(subset))

    for x in subset:
        # check status of data
        status = checkCombStatus(x,quick)

        if status < 2:
            # search data
            searchData(x,session,status,quick)
        
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
    
    score = chooseDisplayData(code,readerCount,Growth,authorScore,pieScore)
    
    # get position of largest n data
    N=len(score)
    largest = sorted(range(len(score)), key=lambda sub: score[sub])[-N:]

    print()
    print("top", N, "combinations")
    # store top N combinations into array
    z=0
    while z < len(largest):
        readers.append(subset[largest[z]])
        comb.append(score[largest[z]])
        print(subset[largest[z]], "=", score[largest[z]])
        z += 1
    print()

    readers.reverse()
    comb.reverse()
    
    # default min = 0, max = 100
    if minval == '':
        minval = 0
    if maxval == '':
        maxval = 100
        
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
        point = (float(x) - min_val)/(max_val - min_val)*100
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

def searchData(x,session,status,quick):
    reader = count = avgreader = pie_score = this = a = 0
    popular_article_list = []
    all_paper = []
    fromYear = 100
    
    # contains all number of publications for all the years
    years = [None] * (fromYear + 1) 
    while a <= fromYear:
        years[a] = 0
        a += 1
	
    min_yr = current_year() - 99
    
    pages = session.catalog.advanced_search(title=x, view="stats", min_year=min_yr, max_year=current_year())
    for page in pages.iter(page_size=100):
        complete = repeat = 0
        
        try:
            yr_diff = current_year() - page.year
        except:
            yr_diff = -1
        
        # if paper type and publish year is valid
        if isLegalType(page) and yr_diff >= 0:
            
            try:
                new_paper = [page.identifiers['doi'], page.reader_count,page.year]
                all_paper.append(new_paper)
            except:
                continue
                
            reader += page.reader_count
            count += 1

            # get popular paper info
            popular_article_list = popular_article(popular_article_list, page.reader_count, page.link, page.title, page.year)
			
            # get paper growth score
            years[yr_diff] += 1
            growth=calcAvgGrowth(years)

            if quick:
                if count >= 100:
                    break

    # get reader count score
    avgreader = round((reader+1) / (count+1),2)
	
    the_data = calcData(all_paper)
    authorscore = the_data['author']
    pieScore = the_data['pie']
    
    #pieScore = 0
    if status != None:
        for i in popular_article_list:
            store_Paper(paper_title=i[2], paper_reader_count=i[0], paper_link=i[1], paper_year_published=i[3])
            store_Paper_subcategory(paper_title=i[2], query_1=x[0], query_2=x[1])
    
        if status == 1:
            # update db
            updateComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=pieScore, quickScore=quick)
        else:
            # insert to db
            insertComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=pieScore, quickScore=quick)
    else:
        os.system('cls')
        
        # get data from calculation
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
    
    # what happens if code = "0000"
    
    for i in code:
        if i == '1':
            displayData.append(temp[j])
        j+=1
    
    for x in range(len(readerCount)):
        tempscore = 0
        for y in displayData:
            tempscore += float(y[x])
        score.append(round((tempscore/len(displayData))))
    
    return score