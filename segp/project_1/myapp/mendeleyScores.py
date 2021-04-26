# file created by group
from .mendeleyScript import *
from paper.db_paper import *
from itertools import combinations
import time
import os

# check if paper is legal
def isLegalType(page):
    legalTypes = ["journal", "book", "generic", "book_section", "working_paper", "thesis"]
    for x in legalTypes:
        if (x == page.type):
            return 1
    return 0

# return paired tuples
def pair_subset(query):
    subset = []
    comb = combinations(query,2)
    for i in comb:
        subset.append(i)
    
    return subset

# return paired tuples and single queries
def all_subset(query):
    subset = query
    subset += pair_subset(query)
    return subset

# calculate and return growth
def calcAvgGrowth(years):
    i = len(years) - 2
    totalGrowth = 0
    while i >= 0:
        totalGrowth += (((years[i] + 1) - (years[i + 1] + 1)) / (years[i + 1] + 1))
        i -= 1
    avgGrowth = round(totalGrowth / (len(years) - 1), 2)
    return avgGrowth

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