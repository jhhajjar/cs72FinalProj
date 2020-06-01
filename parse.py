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
            address += i.text + ' ' 
    return address



# If save_to_files is true, then the speeches will be saved a folder. If not, they will be returned in a list
def parse_all(save_to_files=True):
    if save_to_files:
        if not os.path.exists('sotu_speeches'):
            os.makedirs('sotu_speeches')
    else:
        speeches = []
    # Get all links from this page
    link = 'https://www.presidency.ucsb.edu/documents/presidential-documents-archive-guidebook/annual-messages-congress-the-state-the-union'
    correct_links_to_follow = 'https://www.presidency.ucsb.edu/ws/index.php?pid='
    page = requests.get(link).content
    soup = bs4.BeautifulSoup(page, features='html.parser')
    links = soup.find_all('a')
    # Loop through all links
    for i in links:       
        if str(i.get('href'))[:len(correct_links_to_follow)] == correct_links_to_follow:
            year = re.search('[0-9][0-9][0-9][0-9]', i.contents[0])
            if year and int(year[0]) >= 1900:
                try:
                    print(f'Getting {i.contents[0]}')
                    if save_to_files:
                        f = open(f"sotu_speeches/{i.contents[0]}.txt", "w")
                        f.write(parse_page(str(i.get('href'))))
                        f.close()
                    else:
                        speeches.append(parse_page(str(i.get('href'))))
                except Exception as e:
                    print(e)
                    print(f'Couldnt write {i.contents[0]}. Go find this one manually')

    if not save_to_files:
        return speeches

# TEST
# print(parse_page('https://www.presidency.ucsb.edu/documents/remarks-the-state-the-union-message-key-west-florida'))

parse_all()
