import requests
from bs4 import BeautifulSoup
from pprint import pprint

def getAllLinks(soup):   
    urls = []
    for item in soup.findAll('div',{'class':'g'}):
        link = item.find("a")
        try:
            href = link['href']
            href = href.split("/url?q=")[1]
            urls.append(href)
            new_url = requests.get(href)
            newSoup = BeautifulSoup(new_url.text, "lxml")
            for link in newSoup.findAll("a"):
                print(link)
            # data of all the website

        except:
#             print("{} not available".format(link))
            pass

    return urls



def crawlGooglePages():    
    search_word= "cyberpropaganda"
    base = "http://www.google.com"
    url = "http://www.google.com/search?q="+ search_word

    getting_url = requests.get(url)
    soup = BeautifulSoup(getting_url.text, "lxml")
    footerPageUrls = soup.find('table',{'id':'nav'})
    
    pageUrls = []
    
    for link in footerPageUrls.findAll("a"):
        pageUrls.append(link['href'])
        
    return pageUrls


pageUrls = crawlGooglePages()
base = "http://www.google.com"
allUrls = {}
page = 1
for pageLink in pageUrls:
    getting_url = requests.get(base+pageLink)
    soup = BeautifulSoup(getting_url.text, "lxml")
    pageUrls = getAllLinks(soup)
    allUrls["page-"+str(page)] = pageUrls
    page+=1

# pprint(allUrls)
