"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json


def elsevier_auth():
    ## Initialize client
    client = ElsClient("1ebaeb2ea719e96071ce074a5c341963")
    client.inst_token = "6383ea4db27ea6b7353107935f098932"
    return client

def elsevier_des(keyword):
    client = elsevier_auth()
    #myDocSrch = ElsSearch("TITLE("+paper+")","scopus")
    myDocSrch = ElsSearch(keyword,'sciencedirect')
    myDocSrch.execute(client,get_all = False)

    pii = []
    
    count=0
    
    for i in myDocSrch.results:
        if count < 5:
            try:
                pii.append(i['pii'])
            except:
                pii.append("-")
            count += 1

    paper = []
    
    for j in pii:
        if j != "-":
            pii_doc = FullDoc(sd_pii=j)
            if pii_doc.read(client):
                #print(pii_doc.data['coredata']['prism:coverDisplayDate'])
                
                result = {
                    'name': [],
                    'reader_count': [],
                    'link': [],
                    'year_published': [],
                    'discription': [],
                }
                
                result['name'] = pii_doc.data['coredata']['dc:title']
                result['reader_count'] = 0
                result['link'] = "https://www.sciencedirect.com/science/article/pii/"+j
                year = pii_doc.data['coredata']['prism:coverDate']
                result['year_published'] = year[:4]
                result['discription'] = pii_doc.data['coredata']['dc:description']
                
                paper.append(result)
            print("reading data...")

    paper = {
        'paper': paper,
    }
    
    return paper