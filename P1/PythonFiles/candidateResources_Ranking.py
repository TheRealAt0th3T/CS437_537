
import pandas as pd
import re, string
import time
import json
import math

# start = time.time()
# with open('Computed/wiki_dict.json') as json_file:
#     wiki_dict = json.load(json_file)
# wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id']]
# print(wiki)
# end = time.time()
# print(end - start)

wiki = pd.DataFrame()
wiki_dict = []
CR = pd.DataFrame()

def set(dataframe, dict):
    global wiki, wiki_dict
    wiki = dataframe
    wiki_dict = dict

# Max d computation
# def maxD(content):
#     dict = {}
#     for word in str(content).split(" "):
#         #         print(word)
#         if word in dict.keys():
#             dict[word] += 1
#         else:
#             dict[word] = 1
#     max_value = max(dict.values())
#     #     max_keys = ""
#     #     for k in dict.keys():
#     #         if int(max_value) == int(dict[k]):
#     #             max_keys += str(k) + " "
#     #     print(max_keys)
#     #     print(max_value)
#     #     return max_keys
#     return max_value


# def noMultipleSpace(content):
#     ret = content.split(" ")
#     while ("" in ret):
#         ret.remove("")
#     ret2 = ""
#     for r in ret:
#         ret2 += r + " "
#     #     print(ret2)
#     return ret2


# def noSpaceEnd(content):
#     return content[0:(len(content) - 1)]


# wiki['title'] = wiki['title'].apply(noMultipleSpace)
# wiki['max_occur_words'] = wiki['max_occur_words'].apply(noSpaceEnd)

# wiki['max_occur_words'] = wiki['content'].apply(maxD)
# wiki['max_occur_number'] = wiki['content'].apply(maxD)
# wiki
# wiki.to_csv("wiki.csv")




# start = time.time()
# with open('Computed/wiki_dict.json') as json_file:
#     wiki_dict = json.load(json_file)
# wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id','max_occur_words','max_occur_number']]
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
    global CR
    keys = getRows(qArray)
    CR = wiki.iloc[keys]
    return CR

# CR = containsIDWiki('morocco saudi') # the user is going to enter their query in this function
# CR # this prints info that we will potentially need.
# print(wiki_dict['morocco'])

# print(wiki_dict['morocco'].keys())
# print(wiki_dict['saudi'].keys())

# mor = wiki.iloc[minusOne(list(wiki_dict['morocco'].keys()))]
# sau = wiki.iloc[minusOne(list(wiki_dict['saudi'].keys()))]
# result = pd.merge(mor, sau, on=["id"])
# result

def getFreq(word,doc_id):
#     print("word: " + word)
#     print("doc_id: " + str(doc_id))
    
#     print(str(doc_id) in wiki_dict[word].keys())
#     print(doc_id)
#     print(wiki_dict[word].keys())
    if str(doc_id) in wiki_dict[word].keys():
        return wiki_dict[word][str(doc_id)]
    else:
        return 0

def getMaxd(doc_id):
#     print(doc_id)
    return wiki['max_occur_number'].iloc[doc_id-1]

# print(getMaxd(1))


def getN():
    return len(wiki)

# print(getN())

def getnw(word):
    return len(list(wiki_dict[word].keys()))

# print(getnw('morocco'))

def getTFIDF(word, doc_id):
    try:
        wiki_dict[word]
    except:
        print("word does not exist in our system.")
        return -1
    
    TF = getFreq(word, doc_id)/getMaxd(doc_id)
    IDF = math.log2(getN()/getnw(word))
#     print("TF: " + str(TF))
#     print("freq: "+str(getFreq(word, doc_id)))
#     print(getFreq(word, doc_id))
#     print(getMaxd(doc_id))
    return TF*IDF

# word = "morocco"
# doc_id = 1
# print(getTFIDF(word,doc_id))

def queryWordTFIDF(query):
    global CR
    for word in query.split(" "):
        TIList = []
        for key in getRows(query):
#             print(key)
            TIList.append(getTFIDF(word, key+1))
        CR[word] = TIList
    first = True
    for word in query.split(" "):
        if first:
            CR['Total'] = CR[word]
            first = False
        else:
            CR['Total'] = CR['Total'] + CR[word]

def setCF(query):
    global CR
    CR = containsIDWiki(query)

def getRelevantResources(query):
    global CR
    setCF(query)
    queryWordTFIDF(query)
    sorted = CR.sort_values(by=["Total"], ascending=False)[['content', 'title', 'id', 'Total']]
    return sorted.head(50)

