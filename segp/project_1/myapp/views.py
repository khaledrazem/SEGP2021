from django.shortcuts import render,redirect
from .mendeleyScores import scoresList

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

def results1(request):
    if request.method == 'POST':
        query = str(request.POST['input_submitted']).split("\\n")
        query.remove("")
    context = scoresList(queryList=query, fromYear=10)
    return render(request, 'Results1.html',context)

def results2(request):
    return render(request, 'Results2.html')