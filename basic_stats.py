import sqlite3
import collections

def pretty_print(dictionary):
    for k, v in dictionary.items():
        print(f"{k} : {v}")


con = sqlite3.connect("zotero.sqlite")
cur = con.cursor()

#fulltextItemWords gives you every word in your indexed database


res = cur.execute("SELECT itemTypeID, typeName from itemTypes")
item_dict = {k : v for (k, v) in res.fetchall()} #mapping between item type id and actual names of item types

res = cur.execute("SELECT wordID, word from fulltextWords")
word_dict = {k : v for (k, v) in res.fetchall()} # mapping between word id and actual words

# TODO: map from item id to metadata, etc

# res = cur.execute("SELECT wordID from fulltextItemWords")
# word_dump = [k[0] for k in res.fetchall()]
# item_counts = {}
# for item in item_types:
#     clean_item = item[0]
#     if item_dict[clean_item] not in item_counts:
#         item_counts[item_dict[clean_item]] = 0
#     item_counts[item_dict[clean_item]] += 1
#
# print(len(word_dump))

# more ideas
# total pages indexd, most popular words

## GET STATS ON EACH DOCUMENT TYPE ##
res = cur.execute("SELECT itemTypeID from items")
item_types = [k[0] for k in res.fetchall()]
item_counts = {}
for clean_item in item_types:
    if item_dict[clean_item] not in item_counts:
        item_counts[item_dict[clean_item]] = 0
    item_counts[item_dict[clean_item]] += 1

ordered_item_counts = collections.OrderedDict(sorted(item_counts.items()))
pretty_print(ordered_item_counts)
