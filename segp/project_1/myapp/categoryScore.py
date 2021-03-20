from .mendeleyScores import *
from .author import *
from pytrends.request import TrendReq
from subcategory.db_subcategory_query import *
from combinations.db_subcategory_combination import *
from paper.db_paper import *
from paper.db_paper_subcategory import *
from .elsevier_test import *
import time
import os

def getTrend(subcat,quick,growth_query,authorscore_query,readercount_query,pie_query):
    os.system('cls')
    start = time.time()
    trend = []
    topsubcat = []

    print()
    for x in subcat:
        connection = 0
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
                
            try:
                trenddata = pytrends.interest_over_time()
                connection = 1
            except:
                print("Unable to connect to Google Trends! Try Again Later!")
            
            if connection == 1:
                if not trenddata.empty:
                    this_trend = float(trenddata[x].sum())      # total trend of current week
                else:
                    this_trend = 0       # no trend
            else:
                if status == 0:
                    this_trend = 0

            if status == 1:
                updateSubcat(x, this_trend, quick)    # update db
            else:
                insertSubcat(x, this_trend, quick)    # insert to db

            fake.clear()

        trend.append(this_trend)
    
    
    if len(trend) > 5:
        N = 5
    else:
        N = len(trend)

    i = 0
    
    # get position of largest data
    largest = sorted(range(len(trend)), key=lambda sub: trend[sub])[-N:]
    
    # get top N subcategory
    print()
    print("top", N, "subcategory")
    while i < len(largest):
        print(subcat[largest[i]], "=", trend[largest[i]])
        topsubcat.append(subcat[largest[i]])
        i += 1
    print()

    combinations = pair_subset(topsubcat)
    
    results = {
        'realresult': topCombination(combinations,quick,growth_query,authorscore_query,readercount_query,pie_query),
    }

    end = time.time()
    print("total time used:", end - start, "s")
    print()

    return results

def topCombination(subset,quick,growth_query,authorscore_query,readercount_query,pie_query):
    session = mendeleyAuth()
    readerCount = []
    authorScore = []
    Growth = []
    pieScore = []
    results = {
        'topReader': [],
        'topComb': [],
        'zipped': []
    }
    i = 0
    N = 10

    for x in subset:
    
        # check status of data
        status = checkStatus(x,quick)

        if status < 2:
            searchData(x,session,status,quick)
        
        comb_result = selectComb(query_1=x[0], query_2=x[1])    # get data from db
        readerCount.append(comb_result.combination_score)
        authorScore.append(comb_result.combination_authorscore)
        Growth.append(comb_result.combination_growth)
        pieScore.append(comb_result.combination_pie)
        
    tempscore = []
    
    readerCount = data_norm(readerCount)
    Growth = data_norm(Growth)
    #pieScore = data_norm(pieScore)
    #authorScore = data_norm(authorScore)
    
    # choose which data to display
    score = chooseDisplayData(readercount_query,growth_query,authorscore_query,pie_query,readerCount,Growth,authorScore,pieScore)
    
    # get position of largest data
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

    results['topReader'].reverse()
    results['topComb'].reverse()
    results['zipped'] = zip(results['topReader'], results['topComb'])

    return results

def filterSubcat(q1,q2,minval,maxval,code,quick):
    os.system('cls')
    start = time.time()
    
    results = {
        'realresult': filterResult(q1,q2,minval,maxval,code,quick)
    }
    
    end = time.time()
    print("total time used:", end - start, "s")
    print()
    
    return results

def filterResult(q1,q2,minval,maxval,fakecode,quick):
    subset = []
    
    session = mendeleyAuth()
    readerCount = []
    Growth = []
    pieScore = []
    authorScore = []
    results = {
        'topReader': [],
        'realReader': [],
        'topComb': [],
        'realComb': [],
        'zipped': [],
    }
    
    readers=[]
    comb=[]
    i = 0
    
    # find all subcategory combination
    all_comb = pair_subset(q2)
    
    if not q1:
        subset = all_comb
    else:
        # keep checked subcategory
        for p in all_comb:
            for q in q1:
                if p[0] == q or p[1] == q:
                    subset.append(p)
        subset = list(dict.fromkeys(subset))

    for x in subset:
    
        # check status of data
        status = checkStatus(x,quick)

        if status < 2:
            searchData(x,session,status,quick)
            
        
        comb_result = selectComb(query_1=x[0], query_2=x[1])    # get data from db
        readerCount.append(comb_result.combination_score)
        authorScore.append(comb_result.combination_authorscore)
        Growth.append(comb_result.combination_growth)
        pieScore.append(comb_result.combination_pie)

    readerCount = data_norm(readerCount)
    Growth = data_norm(Growth)
    #pieScore = data_norm(pieScore)
    #authorScore = data_norm(authorScore)
    
    code = list(fakecode)
    
    if code[0] == '1':
        readercount_query = True
    else:
        readercount_query = False
        
    if code[1] == '1':
        growth_query = True
    else:
        growth_query = False
        
    if code[2] == '1':
        authorscore_query = True
    else:
        authorscore_query = False
        
    if code[3] == '1':
        pie_query = True
    else:
        pie_query = False
    
    score = chooseDisplayData(readercount_query,growth_query,authorscore_query,pie_query,readerCount,Growth,authorScore,pieScore)
    
    N=len(score)

    # get position of largest data
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
    
    if minval == '':
        minval = 0
    
    if maxval == '':
        maxval = 100
    
    if minval == maxval:
        m = [pos for pos, val in enumerate(comb) if val == float(minval)]
        if m:
            q = 0
            while q < len(m):
                results['realReader'].append(readers[m[q]])
                results['realComb'].append(comb[m[q]])
                q += 1
        else:
            results['realReader'] = readers
            results['realComb'] = comb
    else:
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

    return results

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

def searchKeyword(keyword,quick):
    os.system('cls')
    session = mendeleyAuth()
    results = {
        'reader': [],
        'author': [],
        'growth': []
    }
    
    i = 0
    N = 10

    popular_article_list=[]
    reader = count = avgreader = this = 0
    
    pages = session.catalog.advanced_search(title=keyword, view="stats")
    authorList=[]
    fname = []
    lname = []
    
    a = 0
    fromYear=500
    years = [None] * (fromYear + 1)  # contains all number of publications for all the years
    while a <= fromYear:
        years[a] = 0
        a += 1
    
    for page in pages.iter(page_size=100):
        complete = 0
        if isLegalType(page):
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
                    
                    lenfirst = len(first_name)
                    lenlast = len(last_name)
                    
                    if lenlast < 2 or lenfirst < 2:
                        complete = 0
                    else:
                        complete = 1
                    
                    if complete == 1:
                        name = first_name + " " + last_name

                        for y in authorList:
                            if y == name:
                                repeat += 1
                                continue
                        
                        if repeat == 0:     
                            authorList.append(name)
                            fname.append(first_name)
                            lname.append(last_name)
            
            popular_article_list = popular_article(popular_article_list, page.reader_count, page.link, page.title, page.year)
            
            if page.year == None or page.year > current_year():
                pubyear = current_year()
            else:
                pubyear = page.year
            
            index = current_year() - pubyear
            years[index] += 1
            
            growth=calcAvgGrowth(years)
            
            if quick:
                if count >= 100:
                    break
    
    avgreader = round((reader+1) / (count+1),2)
    
    """
    num_of_author = len(authorList)
    print(num_of_author,"authors, estimated completion time =", (num_of_author*7)/60,"minutes")
    print()
    authorscore = author_score(fname,lname)
    """
    
    authorscore = 0

    readerCount = avgreader      # get data from calc
    authorScore = authorscore
    Growth = growth
    
    results['reader'] = readerCount
    results['author'] = authorScore
    results['growth'] = Growth
    
    return results



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

def checkStatus(x,quick):
    if isinCombDB(query_1=x[0],query_2=x[1]):
        comb_result = selectComb(query_1=x[0],query_2=x[1])
        if (isCombUpdated(query_1=x[0],query_2=x[1])==False) or (comb_result.quick_search_data != quick):
            status = 1      # in db but not updated
        else:
            status = 2      # in db and is updated
    else:
        status = 0      # not in db

    return status

def searchData(x,session,status,quick):
    
    popular_article_list=[]
    reader = count = avgreader = pie_score = this = 0

    pages = session.catalog.advanced_search(title=x, view="stats")
    authorList=[]
    fname = []
    lname = []
	
    a = 0
    fromYear=500
    years = [None] * (fromYear + 1)  # contains all number of publications for all the years
    while a <= fromYear:
        years[a] = 0
        a += 1
	
    for page in pages.iter(page_size=100):
        complete = 0
        if isLegalType(page):
            """
            try:
                pie_score += pie(page.identifiers['doi'],page.reader_count,page.year)
            except:
                pie_score += 0
            """
            pie_score+=0
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

                    lenfirst = len(first_name)
                    lenlast = len(last_name)

                    if lenlast < 2 or lenfirst < 2:
                        complete = 0
                    else:
                        complete = 1

                    if complete == 1:
                        name = first_name + " " + last_name

                    for y in authorList:
                        if y == name:
                            repeat += 1
                            continue

                    if repeat == 0 and complete == 1:     
                        authorList.append(name)
                        fname.append(first_name)
                        lname.append(last_name)

            popular_article_list = popular_article(popular_article_list, page.reader_count, page.link, page.title, page.year)
			
            if page.year == None or page.year > current_year():
                pubyear = current_year()
            else:
                pubyear = page.year
			
            index = current_year() - pubyear
            years[index] += 1

            growth=calcAvgGrowth(years)

            if quick:
                if count >= 100:
                    break
	
    avgreader = round((reader+1) / (count+1),2)
    for i in popular_article_list:
        store_Paper(paper_title=i[2], paper_reader_count=i[0], paper_link=i[1], paper_year_published=i[3])
        store_Paper_subcategory(paper_title=i[2], query_1=x[0], query_2=x[1])
	
    """
    num_of_author = len(authorList)
    print(num_of_author,"authors, estimated completion time =", (num_of_author*7)/60,"minutes")
    print()
    authorscore = author_score(fname,lname)
    """
	
    authorscore = 0

    if status == 1:
        updateComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=round(pie_score,2), quickScore=quick)  # update db
    else:
        insertComb(query_1=x[0],query_2=x[1], readercount=round(avgreader, 2), authorscore=authorscore, growth=round(growth, 2),pie_score=round(pie_score,2), quickScore=quick)  # insert to db

def chooseDisplayData(readercount_query,growth_query,authorscore_query,pie_query,readerCount,Growth,authorScore,pieScore):
    if readercount_query and growth_query and authorscore_query:
        score = readerCount
    else:
        if readercount_query and growth_query:
            zipped_lists = zip(readerCount, Growth)
            score = [(float(x) + float(y))/2 for (x, y) in zipped_lists]
        elif readercount_query and authorscore_query:
            zipped_lists = zip(readerCount, authorScore)
            score = [(float(x) + float(y))/2 for (x, y) in zipped_lists]
        elif growth_query and authorscore_query:
            zipped_lists = zip(authorScore, Growth)
            score = [(float(x) + float(y))/2 for (x, y) in zipped_lists]
        elif readercount_query:
            score = readerCount
        elif growth_query:
            score = Growth
        elif authorscore_query: 
            score = authorScore
        elif pie_query:
            score = pieScore
        else:
            score = readerCount
    
    return score