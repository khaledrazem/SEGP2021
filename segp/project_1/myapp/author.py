from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import time

def elsevier_auth():
    client = ElsClient("1ebaeb2ea719e96071ce074a5c341963")
    client.inst_token = "6383ea4db27ea6b7353107935f098932"
    return client

def author_score(fname, lname):
    client = elsevier_auth()
    
    the_zip = zip(fname,lname)
    num = len(fname)
    count = 0
    total = 0
    score = 0
    
    for first, last in the_zip:
        start = time.time()
        print(first,last)
        myDocSrch = ElsSearch('AUTHLASTNAME('+last+') AND AUTHFIRST('+first+')','author')
        myDocSrch.execute(client)
        
        for x in myDocSrch.results:
            try:
                a_id = x['dc:identifier']
            except:
                continue
            auth_id = a_id.replace('AUTHOR_ID:','')
            
            author = ElsAuthor(author_id = auth_id)
            if(author.read_metrics(client)):
                h_index = author.data['h-index']
                score += h_index
                print(first,last," ID:",auth_id," h-index:",h_index)
            else:
                print("no data")
                score += 0
        
        end = time.time()
        diff = end - start
        total += diff
        count += 1
        num -= 1
        avg =  total/count
        est = (num*avg)/60
        print("time used for this author:", end - start, "s")
        print(num,"authors, estimated time left:",est,"minutes")
        print()
    return score

