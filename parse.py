import bs4
import requests, re, os
#
# URL TO GET THINGS FROM : https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union
# example: https://www.presidency.ucsb.edu/documents/address-before-joint-session-the-congress-the-state-the-union-27

def parse_page(link):
    page = requests.get(link).content
    soup = bs4.BeautifulSoup(page, features='html.parser')
    
    links = soup.find(attrs={"class": "field-docs-content"} )
    address = ''
    for i in links.contents:
        if type(i) == bs4.element.Tag:
            address += i.text    
    return address



# If save_to_files is true, then the speeches will be saved a folder. If not, they will be returned in a list
def parse_all(save_to_files=True):
    if save_to_files:
        if not os.path.exists('sotu_speeches'):
            os.makedirs('sotu_speeches')
    link = 'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union'
    correct_links_to_follow = 'https://www.presidency.ucsb.edu/ws/index.php?pid='
    page = requests.get(link).content
    soup = bs4.BeautifulSoup(page, features='html.parser')
    links = soup.find_all('a')
    for i in links:       
        if str(i.get('href'))[:len(correct_links_to_follow)] == correct_links_to_follow:
            if len(i.contents[0]) == 4 and int(i.contents[0]) >= 1900:
                try:
                    f = open(f"sotu_speeches/{i.contents[0]}.txt", "w")
                    f.write(parse_page(str(i.get('href'))))
                    f.close()
                except:
                    print(f'Couldnt write {i.contents[0]}. Go find this one manually')

# TEST
print(parse_page('https://www.presidency.ucsb.edu/documents/address-before-joint-session-the-congress-the-state-the-union-27'))

parse_all()
