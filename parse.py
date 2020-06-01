import bs4
import requests
#
# URL TO GET THINGS FROM : https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union
# example: https://www.presidency.ucsb.edu/documents/address-before-joint-session-the-congress-the-state-the-union-27

def parse_page(link):
    page = requests.get(link).content
    soup = bs4.BeautifulSoup(page, features='html.parser')
    
    links = soup.find(attrs={"class": "field-docs-content"} )
    address = ''
    tags =['<p>','</p>','<i>', '<i/>']
    for i in links.contents:
        to_append = str(i)
        for j in tags:
            to_append = to_append.replace(j,'')
        address += to_append
    
    return address

print(parse_page('https://www.presidency.ucsb.edu/documents/address-before-joint-session-the-congress-the-state-the-union-27'))