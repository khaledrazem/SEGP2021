from bs4 import BeautifulSoup
import requests
    
def categoryscraper(cat):

    temp=cat

    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }
    
    url="https://scholar.google.com/citations?view_op=top_venues&hl=en&vq="+temp    #scholar url and temp is the url code for the category


    response = requests.get(url,headers=headers)    #must have header to not get blocked

    soup = BeautifulSoup(response.content,'lxml')

    storing = False   #trigger so it doesnt print menu title, (sign in, and "subcategories"

    categories_arr= []
    
    #filter out tags to get number of citations and title
    for item in soup.select('a.gs_md_li',{"tabindex":"-1"}):    #item is string of subcategory, parameters are tags of wanted fields(as can be seen in inspect element)
        try:
            item=item.text
            if (storing):
                subcategory = item.replace(" & "," and ")
                categories_arr.append(subcategory)
            if "Subcategories" in item: #start saving data after subcategories field
                storing = True

        except Exception as e:
            print('')
    
    return categories_arr
