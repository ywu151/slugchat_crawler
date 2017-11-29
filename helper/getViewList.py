import requests
from bs4 import BeautifulSoup
import re
import json
import pprint
import time
import random

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

HEADER = {
    'Referer':'http://music.163.com/',
    'Host':'music.163.com',
    'User-Agent':'Mozilla/5.0'
}

PROXY = {'http': 'http://115.159.152.130:81', 'https': 'https://115.159.152.130:81'}

TEMP_STORE_SIZE = 20

def getSongList(title_dic, view_lists, playlists, ind, dealed_list):
    playlist_id = playlists[ind]
    dealed_list.add(playlist_id)

    url = 'http://music.163.com/playlist?id=%s' % playlist_id
    getted = False
    req = None
    while not getted:
        try:
            req = requests.get(url=url, headers=HEADER)
            time.sleep(2 + random.randint(0,3))
        except:
            getted = False
        else:
            getted = True

    tr_samples = r'<i>\(([0-9]*)\)</i>'
    samples = re.findall(tr_samples, req.text)
    if len(samples) >= 1:
        samples = int(samples[0]) + 1
    else:
        samples = 1
    bf = BeautifulSoup(req.text)
    title_divs = bf.find_all('ul', class_='f-hide')
    if len(title_divs) == 0: return
    tr_title = r'song\?id=[0-9]{8}">([\u4E00-\u9FA5]*?)</a>'
    titles = re.findall(tr_title, str(title_divs[0]))

    view_list = []
    for title in titles:
        if title in title_dic:
            view_list.append(title_dic[title])

    if len(view_list) < 5 or len(view_list) / len(titles) < 0.1: return

    view_lists[playlist_id] = dict(list=view_list, samples=samples)

    if len(view_lists) % TEMP_STORE_SIZE == 0:
        with open('view_lists.txt', 'w') as outfile:
            json.dump(view_lists, outfile, indent=2)
        print("------ temp store ------")

    playlist_divs = bf.find_all('a', class_='sname f-fs1 s-fc0')
    for playlist_div in playlist_divs:
        try:
            playlist_href = playlist_div.get('href')
            new_playlist_id = playlist_href.split("=")
            new_playlist_id = new_playlist_id[1]
            if new_playlist_id not in dealed_list:
                playlists.append(new_playlist_id)
                dealed_list.add(new_playlist_id)
        except:
            continue
    print("---- view_lists number: %d, queue left number %d ----" % (len(view_lists), len(playlists) - ind - 1))


def getPlayLists():
    browser = webdriver.Chrome()
    print(time.time())
    browser.get('http://music.163.com/#/search/m/?s=儿童故事&type=1000')
    print(time.time())
    frame = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.ID, "g_iframe"))
    )
    print(time.time())
    browser.switch_to.frame(frame)

    page_num = 0
    playlist_ids = []
    while True:
        page_num += 1
        leng = len(playlist_ids)
        for ele in browser.find_elements_by_tag_name("a"):
            tr_playlist_id = r'playlist\?id=([0-9]*)'
            playlist_id = re.findall(tr_playlist_id, ele.get_attribute("href"))
            if len(playlist_id) == 1:
                playlist_ids.append(playlist_id[0])
        add_number = len(playlist_ids) - leng
        print('-- page %d add new playlist number %d--' % (page_num, add_number))
        ele_next = browser.find_element_by_link_text("下一页")
        if ele_next.get_attribute("class").find('disabled') > -1: break
        ele_next.click()
        time.sleep(3)

    with open('inti_playlist_ids.txt', 'w') as outfile:
        json.dump(playlist_ids, outfile, indent=2)
    return playlist_ids


