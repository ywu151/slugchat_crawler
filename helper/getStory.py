from bs4 import BeautifulSoup
import requests
from helper import getContent
import json
import pprint

MAX_STORIES_PER_FILE = 100

def func(target_url, age, sid_dic, stories):
    story_url = getContent.SOURCE + target_url
    getted = False
    req = None
    while not getted:
        try:
            req = requests.get(url=story_url)
        except:
            getted = False
        else:
            getted = True
    bf = BeautifulSoup(req.text)
    title_div = bf.find_all('span', class_='isanav')
    title = title_div[0].string

    if title not in sid_dic:
        story = getContent.func(bf, title)
        if story != None:
            sid = len(sid_dic)
            sid_dic[title] = dict(sid = sid, age3 = False, age4 = False, age5 = False, age6 = False)
            stories[sid] = story
        else: return

    sid_dic[title]["age%d" % age] = True

    if len(stories) >= MAX_STORIES_PER_FILE:
        with open('stories%03d.txt' % (len(sid_dic) / MAX_STORIES_PER_FILE), 'w') as outfile:
            json.dump(stories, outfile, ensure_ascii=False, indent=2)
        stories.clear()

        with open('sid_dic.txt', 'w') as outfile:
            json.dump(sid_dic, outfile, ensure_ascii=False, indent=2)

        print("------ temp result when age: %d ------" % age)


# func('/21/content/dan-da-de-lao-hu-21', 3, {}, {})