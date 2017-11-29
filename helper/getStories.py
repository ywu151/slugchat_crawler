from bs4 import BeautifulSoup
import requests
import pprint
from helper import getStory
import time

def func(age, page_num, sid_dic, stories):
    start_time = time.time()
    story_list_url = 'https://story.beva.com/%d/%d' % (age + 18, page_num)
    getted = False
    req = None
    while not getted:
        try:
            req = requests.get(url = story_list_url)
        except:
            getted = False
        else:
            getted = True
    bf = BeautifulSoup(req.text)
    slist_div = bf.find_all('div', class_='slist')
    if len(slist_div) == 0: return False
    bf = BeautifulSoup(str(slist_div))
    story_divs = bf.find_all('a', class_='')

    for story_div in story_divs:
        getStory.func(story_div.get('href'), age, sid_dic, stories)
    print("--- page%d time cost %.0f seconds, story number: %d ---" %
          (page_num, time.time() - start_time, len(sid_dic)))
    return True


# print(func(3, 2, dict(), dict()))
