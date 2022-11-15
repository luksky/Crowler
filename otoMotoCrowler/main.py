import ssl

import requests
from bs4 import BeautifulSoup

link = 'https://www.otomoto.pl/osobowe/jeep/cherokee?search%5Bfilter_enum_generation%5D=gen-v-2014&search%5Bfilter_enum_fuel_type%5D=petrol'
response = requests.get(link,verify=False)

html_string = BeautifulSoup(response.content, 'html.parser').prettify()
parsed_html = BeautifulSoup(html_string, 'html.parser')
pageTags = parsed_html.find_all("li", {"data-testid" : "pagination-list-item"})
print(len(pageTags))
def getPageContent(link):
    response = requests.get(link, verify=False)
    html_string = BeautifulSoup(response.content, 'html.parser').prettify()
    response=BeautifulSoup(html_string, 'html.parser')
    return response

def getCarLinks(link):

    articleTags = getPageContent(link).find_all("article")
    links = []
    i = 0
    for auctions in articleTags:
        # print("\n\n\n*****************************************************************************" + "\nAukcja nr:" +str(i))
        auctionLink = str(auctions.find("a", href=True)["href"])
        # print(auctionLink)
        if auctionLink[0:30] == "https://www.otomoto.pl/oferta/":
            links.append(auctionLink)
        i = i + 1
    return links

carLinks=[]
for i in range(len(pageTags)):
    linkWithPage=link+'&page='+str(i+1)
    print ('Spooling data from: '+linkWithPage)
    carLinks.extend(getCarLinks(linkWithPage))
    print('\n\n')
print(*carLinks, sep="\n")

for carLink in carLinks:
    articleTags = getPageContent(carLink).find_all("div")
    for params in articleTags:
        param = str(params.find("div", href=True)["parametersArea"])
        print (param)

