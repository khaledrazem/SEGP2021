from .models import Paper
from datetime import datetime

def getCurrentTime():
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d")
    return current_time


# check if data is in database
def isinDB_Paper(paper_title):

    if (Paper.objects.filter(name=paper_title).exists()):
        return True
    else:
        return False


# check if data is updated
def isUpdated_Paper(paper_title):
    last = datetime.strptime(getCurrentTime(), "%Y-%m-%d")
    result = Paper.objects.get(name=paper_title)
    day_diff = (last.date() - result.last_update).days
    if (day_diff <= 14):
        return True
    else:
        return False


# insert to database
def insert_Paper(paper_title,paper_reader_count,paper_link,paper_year_published):
    new_paper = Paper(name=paper_title, reader_count=paper_reader_count,link=paper_link,last_update=getCurrentTime(), year_published=paper_year_published)
    new_paper.save()
    print("insert", paper_title)


# update database
def update_Paper(paper_title,paper_reader_count,paper_link, paper_year_published):
    result = Paper.objects.get(name=paper_title)
    result.reader_count = paper_reader_count
    result.link = paper_link
    result.last_update = getCurrentTime()
    result.year_published = paper_year_published
    result.save()
    print("update",  paper_title)


# get data from database
def select_Paper(paper_title):
    if isValid_Paper(paper_title):
        result = Paper.objects.get(name=paper_title)
        return result
    else:
        return False

def isValid_Paper(paper_title):
    if (isinDB_Paper(paper_title)):
        if (isUpdated_Paper(paper_title)):
            return True
    return False

def store_Paper(paper_title,paper_reader_count,paper_link,paper_year_published):
    if isinDB_Paper(paper_title):
        if (isUpdated_Paper(paper_title) == False):
            update_Paper(paper_title,paper_reader_count,paper_link,paper_year_published)
    else:
        insert_Paper(paper_title, paper_reader_count, paper_link,paper_year_published)
