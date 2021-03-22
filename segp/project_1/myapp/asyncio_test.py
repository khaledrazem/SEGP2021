from mendeleyScript import *
from elsapy.elsclient import ElsClient
from elsapy.elsprofile import ElsAuthor, ElsAffil
from elsapy.elsdoc import FullDoc, AbsDoc
from elsapy.elssearch import ElsSearch
import asyncio
import time


def elsevier_auth():
    ## Initialize client
    client = ElsClient("1ebaeb2ea719e96071ce074a5c341963")
    client.inst_token = "6383ea4db27ea6b7353107935f098932"
    return client


def pie(doi, rc, year):
    client = elsevier_auth()
    myDoc = ElsSearch("DOI(" + doi + ")", "scopus")
    myDoc.execute(client, get_all=False)

    if len(myDoc.results[0]) > 2:
        year_diff = current_year() - year
        temp = int(myDoc.results[0]['citedby-count']) / rc
        if year_diff > 0:
            point = round(temp / year, 5)
            print("%35s\t%5d\t%5s\t%3.5f" % (doi, rc, myDoc.results[0]['citedby-count'], point))
        else:
            point = round(temp, 5)
            print("%35s\t%5d\t    0\t%3.5f" % (doi, rc, point))
    else:
        point = 0

    # print("DOI:",doi," RC:",rc,"rc"," cited",myDoc.results[0]['citedby-count']," score:",point)

    return point

async def search(myDoc,client):
    myDoc.execute(client, get_all=False)
    return myDoc.results

async def get_pie(client,i):
    myDoc = ElsSearch("DOI(" + i[0] + ")", "scopus")
    Z = await search(myDoc,client)

    return Z

async def test():
        import timeit

        start = timeit.default_timer()

        client = elsevier_auth()
        tasks = []
        for i in paper:
            task = asyncio.ensure_future(get_pie(client, i))
            tasks.append(task)

        view_counts = await asyncio.gather(*tasks)

        stop = timeit.default_timer()

        print('Time: ', stop - start)


session = mendeleyAuth()

pages = session.catalog.advanced_search(title="artificial intelligence", view="stats")
counts = 0
paper = []
for page in pages.iter(page_size=100):
    try:
        new_paper = [page.identifiers['doi'], page.reader_count,page.year]
        paper.append(new_paper)
        counts+=1;
    except (KeyError,TypeError):
        print("0")

    if counts>20:
        break

for i in paper:
    print(i)

import timeit

start = timeit.default_timer()
client = elsevier_auth()
for i in paper:
    myDoc = ElsSearch("DOI(" + i[0] + ")", "scopus")
    myDoc.execute(client, get_all=False)


stop = timeit.default_timer()

print('Time: ', stop - start)

# asyncio.run(test())



