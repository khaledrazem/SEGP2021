# file created by django and modified by group
from django.shortcuts import render,redirect
from .mendeleyScores import *
from .mendeleyScript import *
from .categoryScore import getTrend, filterResult, searchData, getCode
from .categoryscraper import categoryscraper
from combinations import db_topic_combination
from paper import db_paper_topic
from .drawGraph import *
from .nlp_test import *
from .elsevier_test import elsevier_des,elsevier_auth
import os

# Create your views here.
def home(request):
    os.system('cls')
    return render(request, 'WebsiteSEGP.html')

def results1(request):
    keyword = []

    if request.method == 'GET':
        request_keys = request.GET.keys()
        authorscore_query = 'case_1_form_author' in request.GET
        growth_query = 'case_1_form_quick_trend_growth' in request.GET
        readercount_query = 'case_1_form_average_reader_count' in request.GET
        pie_query = 'case_1_form_paper_impact_effectiveness' in request.GET

        for i in request_keys:
            if "query" in i:
                keyword.append(request.GET[i].replace('\t',''))
        code = getCode(readercount_query, growth_query, authorscore_query, pie_query)
        query_result = getTrend(keyword, code)

    # filter function
    if request.method == 'POST':
        query_A=[]
        keys=list(request.POST.keys())
        for i in keys:
            if "A_" in i:
                query_A.append(i.replace("A_",""))
            if "B_" in i:
                keyword.append(i.replace("B_",""))
            if "min_val" in i:
                minval = request.POST['min_val']
            if "max_val" in i:
                maxval = request.POST['max_val']
            elif "thiscode" in i:
                code = request.POST['thiscode']
        
        query_result = filterResult(query_A,keyword,minval,maxval,code)
    
    context = {
        'query_list': keyword,
        'scores_result': query_result,
        'code': code,
    }
    
    os.system('cls')
    return render(request, 'Results_1.html',context)

def results2(request):
    categories = []
    
    # search function
    if request.method == 'GET':
        query = str(request.GET['case_2_form_query'])
        growth_query = 'case_2_form_quick_trend_growth' in request.GET
        authorscore_query = 'case_2_form_author' in request.GET
        readercount_query = 'case_2_form_average_reader_count' in request.GET
        pie_query = 'case_2_form_paper_impact_effectiveness' in request.GET
        
        categories = categoryscraper(query)
        code = getCode(readercount_query,growth_query,authorscore_query,pie_query)
        subcategory = getTrend(categories, code)
    
    # filter function
    if request.method == 'POST':
        query_A=[]
        keys=list(request.POST.keys())
        for i in keys:
            if "A_" in i:
                query_A.append(i.replace("A_",""))
            if "B_" in i:
                categories.append(i.replace("B_",""))
            elif "min_val" in i:
                minval = request.POST['min_val']
            elif "max_val" in i:
                maxval = request.POST['max_val']
            elif "thiscode" in i:
                code = request.POST['thiscode']
        
        subcategory = filterResult(query_A,categories,minval,maxval,code)
    
    context = {
        'subcategories_list': categories,
        'subcategories': subcategory,
        'code': code,
    }
    
    os.system('cls')
    return render(request, 'Results_2.html',context)

def single_keyword_result(request):
    if request.method == 'GET':
        query = str(request.GET['keyword'])
        
        # define authentication
        session = mendeleyAuth()
        client = elsevier_auth()
        
        # search data
        results = searchData(query,client,session,None)
        
        # get related papers
        try:
            related_paper = db_paper_topic.get_related_paper_with_keyword(query, None)[:5]
        except:
            related_paper = []
        related_paper2 = elsevier_des(query)
        
        # get related words
        related_word = disc(related_paper2['paper'])
        
        # plot graph
        graph = plotGraph(query, None)
        
        context = {
            "keyword": query,
            "results": results,
            "graph": graph,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
        }
    os.system('cls')
    return render(request, 'KeywordAnalysis.html',context)

def keyword_combination_result(request):
    if request.method == 'GET':
        query_1 = str(request.GET['keyword_1'])
        query_2 = str(request.GET['keyword_2'])
        real_query = query_1 + " + " + query_2
        
        # get related papers
        result_keyword = db_topic_combination.selectComb(query_1,query_2)
        related_paper = db_paper_topic.get_related_paper_with_topic_combination(query_1,query_2)[:5]
        related_paper2 = elsevier_des(real_query)
        
        # get related keywords
        related_word = disc(related_paper2['paper'])
        
        # plot graph
        graph = plotGraph(query_1, query_2)
        
        context = {
            "keyword": result_keyword,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
            "graph": graph,
        }
    os.system('cls')
    return render(request, 'TopicAnalysis.html',context)

def error_404(request,exception):
    return render(request, 'Error.html')

def error_500(request):
    return render(request, 'Error.html')