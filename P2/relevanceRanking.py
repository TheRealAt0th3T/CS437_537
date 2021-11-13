import pandas as pd
from PythonFiles import candidate
import json
import math

with open('Computed/wiki_dict.json') as json_file:
    wiki_dict = json.load(json_file)
wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id','max_occur_words','max_occur_number']]

# FREQ
def getFreq(word, doc_id):
    #     print("word: " + word)
    #     print("doc_id: " + str(doc_id))

    #     print(str(doc_id) in wiki_dict[word].keys())
    #     print(doc_id)
    #     print(wiki_dict[word].keys())
    if str(doc_id) in wiki_dict[word].keys():
        return wiki_dict[word][str(doc_id)]
    else:
        return 0


# print(getFreq('morocco', 1))


# MAXD
def getMaxd(doc_id):
#     print(doc_id)
    return wiki['max_occur_number'].iloc[doc_id-1]

# print(getMaxd(1))


# GETN
def getN():
    return len(wiki)

# print(getN())


# GETNW
def getnw(word):
    return len(list(wiki_dict[word].keys()))

# print(getnw('morocco'))


# GETTFIDF
def getTFIDF(word, doc_id):
    try:
        wiki_dict[word]
    except:
        print("word does not exist in our system.")
        return -1

    TF = getFreq(word, doc_id) / getMaxd(doc_id)
    IDF = math.log2(getN() / getnw(word))
    #     print("TF: " + str(TF))
    #     print("freq: "+str(getFreq(word, doc_id)))
    #     print(getFreq(word, doc_id))
    #     print(getMaxd(doc_id))
    return TF * IDF


# NEXT TWO LINES NEED TO BE FIXED
word = "morocco"
doc_id = 1
# print(getTFIDF(word, doc_id))


# QUERY WORDTFIDF
# we should change CR['Total'] (the column name) to something like CR['Relevance Score']
# the reason for this change- it will help the user identify the relevance score if they choose to see the table
def queryWordTFIDF(query):
    for word in query.split(" "):
        TIList = []
        for key in candidate.getRows(query):
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
queryWordTFIDF("morocco saudi") # THIS LINE NEEDS TO BE FIXED
CR.sort_values(by=["Total"], ascending=False)