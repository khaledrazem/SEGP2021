from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch

def elsapy_auth():
    apikey = "7a286322cb3559da3442a03892947ae4"
    insttoken = ""
    client = ElsClient(apikey,insttoken)
    return client

def author_score(queryList):
    client = elsapy_auth()
    
    citation = 0
    
    for author in queryList:
        #client = elsapy_auth()
        auth_srch = ElsSearch("AUTHOR-NAME("+author+")","scopus")
        auth_srch.execute(client)
        paper = auth_srch.results
        
        for x in paper:
            try:
                val = int(x['citedby-count'])
                print(val, end="\t")
            except:
                val = 0
            citation += val
        print()
        print("=================================")
        print(author,"=",citation)
        print()
            
        #print(citation)
    
    return citation