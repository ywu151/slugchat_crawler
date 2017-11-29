import json
from helper import getStory
import MySQLdb

# title: {sid, age3, age4, age5, age6}
sid_dic = {}
# sid: {title, content, style}
stories = {}

with open('sid_dic.txt', 'r') as data_file:
    sid_dic.update(json.load(data_file))

for i in range(1, int(len(sid_dic) / getStory.MAX_STORIES_PER_FILE) + 1):
    with open('stories%03d.txt' % i, 'r') as data_file:
        stories.update(json.load(data_file))


# max_len = 0
# for story in stories:
#     if len(story) > max_len:
#         max_len = len(stories[story]['content'])
#
# print(max_len)

db = MySQLdb.connect("slugchat-test.lorabit.com", "root", "password", "slugchat")
cursor = db.cursor()

for title in sid_dic:
    sid = sid_dic[title]['sid']
    story = stories[str(sid)]
    sql = "INSERT INTO slugchat.tbl_stories\
           VALUES (%d, '%s', '%s', '%s', %d, %d, %d, %d )" % \
          (sid + 1, title, story['style'], story['content'].replace('\'', ''), sid_dic[title]['age3'], sid_dic[title]['age4'],
           sid_dic[title]['age5'], sid_dic[title]['age6'])
    print(sql)
    cursor.execute(sql)
    db.commit()