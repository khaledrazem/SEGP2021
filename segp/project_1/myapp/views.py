from django.shortcuts import render,redirect
from .mendeleyScores import scoresList
from .categoryScore import getTrend
from .categoryscraper import categoryscraper

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
    categories =[]
    if request.method == 'GET':
        query = str(request.GET['topics'])
        pub_query = 'publication' in request.GET
        acite_query = 'acite' in request.GET
        cite_query = 'cite' in request.GET
        categories = categoryscraper(query)
        #print(categories)
        if (pub_query):
            print("Publication:" + str(pub_query))
            """ perform calcluation in calculator script """
        if (acite_query):
            print("Author citation:" + str(acite_query))
            """  perform calcluation in calculator script"""
        if (cite_query):
            print("Ciatation:" + str(cite_query))
            """  perform calcluation in calculator script """
    context = {
        #'subcategories' :catScoresList(queryList=categories,fromYear=10)
        'subcategories' :getTrend(categories)
    }
    return render(request, 'Testing.html',context)

def results1(request):
    if request.method == 'POST':
        query = str(request.POST['input_submitted']).split("\\n")
        query.remove("")

    context = {
    
        'scores_result' :scoresList(query, fromYear=10)
    }
    return render(request, 'Results1.html',context)

def results2(request):
    return render(request, 'Results2.html')