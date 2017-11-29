import json
import MySQLdb

stories = {}

for i in range(1, 8):
    with open('stories%03d.txt' % i, 'r') as data_file:
        stories.update(json.load(data_file))

db = MySQLdb.connect("slugchat-test.lorabit.com", "root", "password", "slugchat")
cursor = db.cursor()

for sid in stories:
    if stories[sid]['content'].find('<br/>') >= 0:
        content = stories[sid]['content'].replace('<br/>', '')
        print(int(sid) + 1)
        print(stories[sid]['title'])
        print(content)
        sql = "UPDATE slugchat.tbl_stories SET content='%s' WHERE storyId=%d;" % (content, int(sid) + 1)
        cursor.execute(sql)
        db.commit()