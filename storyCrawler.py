from helper import getStories,getStory
import json
import time

# title: {sid, age3, age4, age5, age6}
sid_dic = {}
# sid: {title, content, style}
stories = {}

with open('sid_dic.txt', 'r') as data_file:
    sid_dic_ = json.load(data_file)
sid_dic.update(sid_dic_)

start_time = time.time()

for age in range(6, 7):
    page_num = 1
    while getStories.func(age, page_num, sid_dic, stories):
        page_num += 1
    print("------ finish age %d ------" % age)

if len(stories) > 0:
    with open('stories%03d.txt' % (len(sid_dic) / getStory.MAX_STORIES_PER_FILE), 'w') as outfile:
        json.dump(stories, outfile, ensure_ascii=False, indent=2)

with open('sid_dic.txt', 'w') as outfile:
    json.dump(sid_dic, outfile, ensure_ascii=False, indent=2)

print("total time cost: %.0f seconds ---" % (time.time() - start_time))

