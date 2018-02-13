#url = "https://ted2srt.org/"

from bs4 import BeautifulSoup
import requests
import time
import os

FILENAME = "tedtalk_thaisub_list.txt"
URL = "https://www.ted.com/talks?language=th&page={}"
first_page = 1
last_page = 35

if os.path.isfile(FILENAME):
    thai_talk = set(open(FILENAME, 'r').read().split('\n'))
else:
    thai_talk = set()

# get all search terms that have Thai subtitles
print("PAGE: ", end='')
for page in range(first_page, last_page+1):
    print(page, end=', ')
    result = requests.get(URL.format(page))
    if result.status_code == 200:
        bs = BeautifulSoup(result.content, 'lxml')
        for element in bs.find_all(name='a', attrs={'class': ' ga-link'}):
            name = element['href'].split('?')[0].split('/')[-1].replace('_', ' ')
            thai_talk.add(name)
    
    time.sleep(30)