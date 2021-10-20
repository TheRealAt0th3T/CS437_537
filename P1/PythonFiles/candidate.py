
import pandas as pd
import re, string
import time
import json
import math

# start = time.time()
with open('Computed/wiki_dict.json') as json_file:
    wiki_dict = json.load(json_file)
wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id']]
# print(wiki)
# end = time.time()
# print(end - start)


# Max d computation
def maxD(content):
    dict = {}
    for word in str(content).split(" "):
        #         print(word)
        if word in dict.keys():
            dict[word] += 1
        else:
            dict[word] = 1
    max_value = max(dict.values())
    #     max_keys = ""
    #     for k in dict.keys():
    #         if int(max_value) == int(dict[k]):
    #             max_keys += str(k) + " "
    #     print(max_keys)
    #     print(max_value)
    #     return max_keys
    return max_value


def noMultipleSpace(content):
    ret = content.split(" ")
    while ("" in ret):
        ret.remove("")
    ret2 = ""
    for r in ret:
        ret2 += r + " "
    #     print(ret2)
    return ret2


def noSpaceEnd(content):
    return content[0:(len(content) - 1)]


# wiki['title'] = wiki['title'].apply(noMultipleSpace)
# wiki['max_occur_words'] = wiki['max_occur_words'].apply(noSpaceEnd)

# wiki['max_occur_words'] = wiki['content'].apply(maxD)
# wiki['max_occur_number'] = wiki['content'].apply(maxD)
# wiki
# wiki.to_csv("wiki.csv")




# start = time.time()
with open('Computed/wiki_dict.json') as json_file:
    wiki_dict = json.load(json_file)
wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id','max_occur_words','max_occur_number']]
# print(wiki)
# end = time.time()
# print(end - start)



def minusOne(array):
    ret = []
    for a in array:
        ret.append(int(a)-1)
    return ret

def getRows(qArray):
    keys = []
    for qWord in qArray.split(" "):
#         print(qWord)
        keys += minusOne(list(wiki_dict[str(qWord)].keys()))
#     print("before: " + str(keys))
    keys = list(dict.fromkeys(keys)) # remove duplicates
    keys.sort()
#     print("after: " + str(keys))
    return keys


# Takes a word, returns all documents as dataframe that contains the word (Wiki)
def containsIDWiki(qArray):
    keys = getRows(qArray)
    return wiki.iloc[keys]

CR = containsIDWiki('morocco saudi') # the user is going to enter their query in this function
CR # this prints info that we will potentially need.
# print(wiki_dict['morocco'])

# print(wiki_dict['morocco'].keys())
# print(wiki_dict['saudi'].keys())

# mor = wiki.iloc[minusOne(list(wiki_dict['morocco'].keys()))]
# sau = wiki.iloc[minusOne(list(wiki_dict['saudi'].keys()))]
# result = pd.merge(mor, sau, on=["id"])
# result