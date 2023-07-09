import requests, json
from bs4 import BeautifulSoup

response = requests.get('https://coloniae.space/static/mycolony_version.json')

soup = BeautifulSoup(response.text, features="html.parser").text

mycolonyversion = json.loads(soup)['mycolony_version']

print(mycolonyversion)

imageslink = 'https://www.apewebapps.com/apps/my-colony/'+mycolonyversion+'/images/'

response = requests.get(imageslink)

soup = BeautifulSoup(response.text, features="html.parser")

links = soup.find_all('a', href=True)

with open('linkslist.txt', 'w') as file:
    for link in links:
        if link['href'][-4:] in ['.png', '.svg']:
            file.write(imageslink+link['href']+'\n')

print('now run:')
print('wget -q -i linkslist.txt\nfind . -name "*.1" -type f -delete')
