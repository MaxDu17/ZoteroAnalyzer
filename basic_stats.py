import sqlite3
import collections
import tqdm

def pretty_print(dictionary, limit = None):
    counter = 0
    for k, v in dictionary.items():
        print(f"{k} : {v}")
        counter += 1
        if limit is not None and counter > limit:
            return

con = sqlite3.connect("zotero.sqlite")
cur = con.cursor()

# for use in ignoring common words in analysis
with open("stopwords.txt", "r") as f:
    STOPWORDS = [s.split("\n")[0] for s in f]

res = cur.execute("SELECT itemTypeID, typeName from itemTypes")
item_dict = {k : v for (k, v) in res.fetchall()} #mapping between item type id and actual names of item types

res = cur.execute("SELECT wordID, word from fulltextWords")
word_dict = {k : v for (k, v) in res.fetchall()} # mapping between word id and actual words

res = cur.execute("SELECT collectionID, collectionName from collections")
collectionID_to_name = {k : v for (k, v) in res.fetchall()} #mapping between the collection id to the name of the collection
name_to_collectionID = {v : k for k, v in collectionID_to_name.items()}

res = cur.execute("SELECT itemID, collectionID from collectionItems")
collection_to_items = {} #typical: given a folder, what is inside?
items_to_collection = {} #inverted: given an element, what are the folders?

# try 45


for (item, collection) in res.fetchall():
    if item not in items_to_collection:
        items_to_collection[item] = list()
    if collection not in collection_to_items:
        collection_to_items[collection] = list()
    items_to_collection[item].append(collection)
    collection_to_items[collection].append(item)

def get_word_counts(cur, stopwords = None, collection_index = None):
    res = cur.execute("SELECT wordID, itemID from fulltextItemWords") #gets all the words in a dump
    word_counts = {}
    for (word, item) in tqdm.tqdm(res.fetchall()):
        if 45 in items_to_collection.get(item, []):
            print('yes')
        # if collection_index is not None and item not in collection_to_items[collection_index]:
        #     print(item)
        #     continue
        if word_dict[word] not in word_counts:
            word_counts[word_dict[word]] = 0
        word_counts[word_dict[word]] += 1
    clean_counts = {k : v for k, v in word_counts.items() if (stopwords is None or k not in stopwords) and not k.isnumeric()}
    sorted_counts = collections.OrderedDict(sorted(clean_counts.items(), key=lambda item: item[1], reverse=True))
    return sorted_counts

def get_attachment_counts(cur):
    res = cur.execute("SELECT itemTypeID from items")
    item_types = [k[0] for k in res.fetchall()]
    item_counts = {}
    for clean_item in tqdm.tqdm(item_types):
        if item_dict[clean_item] not in item_counts:
            item_counts[item_dict[clean_item]] = 0
        item_counts[item_dict[clean_item]] += 1

    ordered_item_counts = collections.OrderedDict(sorted(item_counts.items()))
    return ordered_item_counts

def calculate_total_pages(cur):
    res = cur.execute("SELECT totalPages from fulltextItems")  # gets all the words in a dump
    items = [k[0] for k in res.fetchall() if k[0] is not None]
    total = 0
    for item in items:
        total += item
    return total

print(calculate_total_pages(cur))

sorted_counts = get_word_counts(cur, STOPWORDS) #, collection_index = name_to_collectionID["Whale (already indexed)"])
pretty_print(sorted_counts, 100)

while True:
    s = input("word? ")
    if s in sorted_counts:
        print(sorted_counts[s])

# more ideas
# total pages indexed

## GET STATS ON EACH DOCUMENT TYPE ##

# pretty_print(ordered_item_counts)
