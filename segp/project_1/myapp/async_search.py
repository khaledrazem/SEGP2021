# file created by group
import requests, time
from urllib.parse import quote_plus as url_encode
import aiohttp
import asyncio

def calcData(paper):
    reader_count = []
    year = []
    doi = []
    
    for i in paper:
        doi.append(i[0])
        reader_count.append(i[1])
        year.append(i[2])
    
    # start search with concurrency
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(searchScorpus(doi,reader_count,year))
    loop.close()
    
    return result

async def searchScorpus(doi,reader_count,year):
    score = {
        'pie': 0,
        'author': 0,
    }
    tasks = []
    tasks2 = []
    
    # create a task for each paper
    for i in doi:
        task = asyncio.ensure_future(getPaper(i))
        tasks.append(task)

    # gather the tasks when complete
    paper_result = await asyncio.gather(*tasks)
    
    author=[]
    cited = []
    
    for i in paper_result:
        cited.append(int(i['cited']))
        if i['author'] != "":
            author.append(i['author'])
    
    zip_list = zip(cited,reader_count,year)
    
    # calculate pie for all papers
    for cite,rc,yr in zip_list:
        if rc is None or rc == 0:
            rc = 1
        if yr == 0:
            point = cite/rc
        else:
            point = (cite/rc)/yr
        score['pie'] += round(point,5)
    
    # start tasks for all author
    for j in author:
        task2 = asyncio.ensure_future(getAuthor(j))
        tasks2.append(task2)
    
    # gather the tasks when complete
    author_result = await asyncio.gather(*tasks2)
    
    # calculate the total score
    score['author'] = sum(author_result)
    
    return score

async def getPaper(doi):
    api_key = "1ebaeb2ea719e96071ce074a5c341963"
    inst_token = "6383ea4db27ea6b7353107935f098932"
    based_url = u'https://api.elsevier.com/content/search/'
    index = 'scopus'

    results = {
        'cited': [],
        'author': [],
    }

    headers = {
        "X-ELS-APIKey"  : api_key,
        "X-ELS-Insttoken" : inst_token,
        "Accept"        : 'application/json'
        }
    
    DOI_URL = 'DOI('+doi+')'
    url = based_url + index + '?query=' + url_encode(DOI_URL) + '&view=COMPLETE'
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            result_data = await resp.json()
            
            # get paper citation count
            try:
                results['cited'] = int(result_data['search-results']['entry'][0]['citedby-count'])
            except:
                results['cited'] = 0
                
            # get paper authors
            try:
                results['author'] = result_data['search-results']['entry'][0]['author'][0]['authid']
            except:
                results['author'] = ''
    return results

async def getAuthor(auid):
    api_key = "1ebaeb2ea719e96071ce074a5c341963"
    inst_token = "6383ea4db27ea6b7353107935f098932"
    based_url = u'https://api.elsevier.com/content/search/'
    index = 'author'

    headers = {
        "X-ELS-APIKey"  : api_key,
        "X-ELS-Insttoken" : inst_token,
        "Accept"        : 'application/json'
        }
    
    AUTHOR_URL = 'AU-ID('+auid+')'
    url = based_url + index + '?query=' + url_encode(AUTHOR_URL)
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            result_data = await resp.json()
            try:
                results = int(result_data['search-results']['entry'][0]['document-count'])
            except:
                results = 0
                
    return results
