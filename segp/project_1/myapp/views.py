from django.shortcuts import render,redirect
from .mendeleyScores import *
from .categoryScore import getTrend, filterSubcat, searchKeyword
from .categoryscraper import categoryscraper
from search_keyword import db_keyword_query
from combinations import db_keyword_combination,db_subcategory_combination
from paper import db_paper_keyword,db_paper_subcategory
from paper.models import paper_keyword_relationship
from .drawGraph import *
from .nlp_test import *
from .elsevier_test import elsevier_des

#from django.shortcuts import render,redirect
#from django.core.files.storage import FileSystemStorage

# Create your views here.

def home(request):
    return render(request, 'WebsiteSEGP.html')

def about(request):
    return render(request, 'About.html')

def topic(request):
    return render(request, 'Topics.html')

def case1(request):
    return render(request, 'Case1.html')

def case2(request):
    return render(request, 'Case2.html')

def testing(request):
    categories = []
    
    # search function
    if request.method == 'GET':
        query = str(request.GET['topics'])
        growth_query = 'growth' in request.GET
        authorscore_query = 'authorscore' in request.GET
        readercount_query = 'readercount' in request.GET
        quick = 'quicksearch' in request.GET
        categories = categoryscraper(query)
        subcategory = getTrend(categories, quick, growth_query,authorscore_query,readercount_query)
    
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
        subcategory = filterSubcat(query_A,categories,minval,maxval,True)

    context = {
        'subcategories_list':categories,
        'subcategories': subcategory,
    }
    return render(request, 'Testing.html',context)

def results1(request):
    keyword = []

    if request.method == 'GET':
        query = str(request.GET['input_submitted']).split("\\n")
        query.remove("")
        keyword = query
        quick_search = 'quicksearch' in request.GET
        query_result = getTrend(query, quick_search, False, False, True)
    
    # filter function
    if request.method == 'POST':
        query_A=[]
        keys=list(request.POST.keys())
        for i in keys:
            if "A_" in i:
                query_A.append(i.replace("A_",""))
            if "B_" in i:
                keyword.append(i.replace("B_",""))
            elif "min_val" in i:
                minval = request.POST['min_val']
            elif "max_val" in i:
                maxval = request.POST['max_val']
        
        query_result = filterSubcat(query_A,keyword,minval,maxval,True)
    
    context = {
        'query_list':keyword,
        'scores_result':query_result,
    }
    return render(request, 'Results1.html',context)

def results2(request):
    if request.method == 'GET':
        query_1 = str(request.GET['category_1'])
        query_2 = str(request.GET['category_2'])
    return render(request, 'Results2.html')

def single_category(request):
    if request.method == 'GET':
        query = str(request.GET['category'])
        
        results = searchKeyword(query,True)
        related_paper = db_paper_subcategory.get_related_paper_with_keyword(query, None)[:5]
        related_paper2 = elsevier_des(query)
        related_word = disc(related_paper2['paper'])
        graph = plotGraph(query, None)
        
        context = {
            "keyword":query,
            "results":results,
            "graph": graph,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
        }
    return render(request, 'SingleCategoryResult.html',context)

def single_keyword_result(request):
    if request.method == 'GET':
        query = str(request.GET['keyword'])
        
        results = searchKeyword(query,True)
        related_paper = db_paper_subcategory.get_related_paper_with_keyword(query, None)[:5]
        related_paper2 = elsevier_des(query)
        related_word = disc(related_paper2['paper'])
        
        graph = plotGraph(query, None)
        
        context = {
            "keyword":query,
            "results":results,
            "graph": graph,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
        }

    return render(request, 'SingleKeywordResult.html',context)

def keyword_combination_result(request):
    if request.method == 'GET':
        query_1 = str(request.GET['keyword_1'])
        query_2 = str(request.GET['keyword_2'])
        real_query = query_1 + " + " + query_2
        
        #result_keyword = db_keyword_combination.db_select_KeywordCombination(query_1,query_2)
        #related_paper = db_paper_keyword.get_related_paper_with_keyword_combination(query_1,query_2)
        result_keyword = db_subcategory_combination.selectComb(query_1,query_2)
        related_paper = db_paper_subcategory.get_related_paper_with_subcategory_combination(query_1,query_2)[:5]
        related_paper2 = elsevier_des(real_query)
        related_word = disc(related_paper2['paper'])
        graph = plotGraph(query_1, query_2)
        
        context = {
            "keyword": result_keyword,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
            "graph": graph,
        }
    return render(request, 'KeywordCombination.html',context)

def subcategory_combination_result(request):
    if request.method == 'GET':
        query_1 = str(request.GET['subcategory_1'])
        query_2 = str(request.GET['subcategory_2'])
        real_query = query_1 + " + " + query_2
        
        result_keyword = db_subcategory_combination.selectComb(query_1,query_2)
        related_paper = db_paper_subcategory.get_related_paper_with_subcategory_combination(query_1,query_2)[:5]
        related_paper2 = elsevier_des(real_query)
        related_word = disc(related_paper2['paper'])
        graph = plotGraph(query_1, query_2)
        
        context = {
            "keyword": result_keyword,
            "related": related_paper,
            "related2": related_paper2,
            "related_word": related_word,
            "graph": graph,
        }
    return render(request, 'SubcategoryCombination.html',context)