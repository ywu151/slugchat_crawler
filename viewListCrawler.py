import json
import MySQLdb
from helper import getViewList

# title: sid
title_dic = {}

db = MySQLdb.connect("slugchat-test.lorabit.com", "root", "password", "slugchat")
cursor = db.cursor()

sql = "SELECT storyId, entityName FROM slugchat.tbl_stories"
cursor.execute(sql)
results = cursor.fetchall()
for row in results:
    title_dic[row[1]] = row[0]

# username: {list: list of sid, samples: int}
view_lists = {}

# playlists = getViewList.getPlayLists()
with open('inti_playlist_ids.txt', 'r') as data_file:
    playlists = json.load(data_file)

dealed_list = set(playlists)

ind = 0

while len(playlists) > ind:
    getViewList.getSongList(title_dic, view_lists, playlists, ind, dealed_list)
    ind += 1

with open('view_lists_finial.txt', 'w') as outfile:
    json.dump(view_lists, outfile, indent=2)



