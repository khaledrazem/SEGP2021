"""An example program that uses the elsapy module"""

from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import json


def elsevier_auth():
    ## Initialize client
    client = ElsClient("7a286322cb3559da3442a03892947ae4")
    client.inst_token = ""
    return client

def find_abstract(doi):
    client = elsevier_auth()
    ## ScienceDirect (full-text) document example using DOI
    doi_doc = FullDoc(doi=doi)
    if doi_doc.read(client):
        print("doi_doc.title: ", doi_doc.title)
        print("doi_doc.abstract: ", doi_doc.data['coredata']['dc:description'])
        doi_doc.write()
    else:
        print("Read document failed.")

# client = elsevier_auth()
# myDocSrch = ElsSearch('Transportation + Architecture','scidir')
# if myDocSrch.execute(client):
#     print(myDocSrch.results)
