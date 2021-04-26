# file created by group
from .mendeleyScript import current_year
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json

import requests, time
from urllib.parse import quote_plus as url_encode
import aiohttp
import asyncio

def elsevier_auth():
    # Initialize client
    client = ElsClient("1ebaeb2ea719e96071ce074a5c341963")
    client.inst_token = "6383ea4db27ea6b7353107935f098932"
    return client

def elsevier_des(keyword):
    client = elsevier_auth()
    
    # search data from elsevier
    myDocSrch = ElsSearch(keyword,'sciencedirect')
    myDocSrch.execute(client,get_all = False)

    doi = []
    
    # search data of all papers
    for i in myDocSrch.results:
        try:
            doi.append(i['prism:doi'])
        except:
            pass
            
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(searchPaper(doi))
    loop.close()

    return result

async def searchPaper(doi):
    tasks = []
    
    # start task for each paper
    for i in doi:
        task = asyncio.ensure_future(getResult(i))
        tasks.append(task)
    
    # gather all completed tasks
    paper_result = await asyncio.gather(*tasks)
    paper = []
    
    data = {
        'name': [],
        'reader_count': [],
        'link': [],
        'year_published': [],
        'discription': [],
    }
    
    for j in paper_result:
        if j['name'] != []:
            paper.append(j)

    all_paper = {
        'paper': paper,
    }
    return all_paper
    
async def getResult(doi):
    api_key = "1ebaeb2ea719e96071ce074a5c341963"
    inst_token = "6383ea4db27ea6b7353107935f098932"
    based_url = u'https://api.elsevier.com/content/search/'
    index = 'scopus'

    headers = {
        "X-ELS-APIKey"  : api_key,
        "X-ELS-Insttoken" : inst_token,
        "Accept"        : 'application/json'
    }

    DOI_URL = 'DOI('+doi+')'
    url = based_url + index + '?query=' + url_encode(DOI_URL) + '&view=COMPLETE'

    results = {
        'name': [],
        'reader_count': [],
        'link': [],
        'year_published': [],
        'discription': '',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            result_data = await resp.json()
            # get the data of paper
            try:
                results['name'] = result_data['search-results']['entry'][0]['dc:title']
                results['reader_count'] = result_data['search-results']['entry'][0]['citedby-count']
                results['link'] = "https://www.sciencedirect.com/science/article/pii/"+result_data['search-results']['entry'][0]['pii']
                results['year_published'] = result_data['search-results']['entry'][0]['prism:coverDate'][:4]
                results['discription'] = result_data['search-results']['entry'][0]['dc:description']
            except:
                pass
    return results

