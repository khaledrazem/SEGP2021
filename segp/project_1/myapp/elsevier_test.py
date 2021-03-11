# """An example program that uses the elsapy module"""
# from elsapy.elsclient import ElsClient
# from elsapy.elsprofile import ElsAuthor, ElsAffil
# from elsapy.elsdoc import FullDoc, AbsDoc
# from elsapy.elssearch import ElsSearch
# from collections import Counter
# import json
#
#
# def elsevier_auth():
#     client = ElsClient("1ebaeb2ea719e96071ce074a5c341963")
#     client.inst_token = "6383ea4db27ea6b7353107935f098932"
#     return client
#
# client = elsevier_auth()
# myDocSrch = ElsSearch('Transportation + Architecture','sciencedirect')
# myDocSrch.execute(client,get_all = False)
# document_doi =[]
# for i in myDocSrch.results:
#     print(i['dc:title'])
#     document_doi.append(i['pii'])
# text=''
# for j in document_doi:
#     pii_doc = FullDoc(sd_pii=j)
#     if pii_doc.read(client):
#         text += pii_doc.data['coredata']['dc:description']
# print(text)
# # split_it = text.split()
# # Counter = Counter(split_it)
# # most_occur = Counter.most_common(40)
# # print(most_occur)
# # pii_doc.data['coredata']['dc:description']
#         # prism: coverDisplayDate
