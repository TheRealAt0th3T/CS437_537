
from nltk.corpus.reader.conll import ConllSRLInstanceList
import pandas as pd
import re, string
import time
import json
import math
from nltk import tokenize
import numpy as np

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
    # print(dataframe)
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
    # print("Contains ID WIKI ")
    # print(CR)
    # print(CR.info())
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
        # print("**************************************************")
        # print(TIList)
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
    # print(CR.info())
    # sorted = CR.sort_values(by=["Total"], ascending=False)[['content', 'title', 'id', 'Total']]
    # return sorted.head(50)
    return CR

########################################################################### method section

def getNumSentences(content):
    return len(tokenize.sent_tokenize(content))

def removeSpace(query):
    ret = query.split(" ")
    while "" in ret:
        ret.remove("")
    retStr = ""
    for c in ret:
        retStr += c + " "
    return retStr[0:len(retStr)-1]

def removeSpaceArray(query):
    while "" in query:
        query.remove("")
    return query

def remove_punc_dot(string_has_punc): ## Leaves . so that we can recognize sentences
    no_punc_result = re.sub('[-=+–,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'》\r\n\t]', '', str(string_has_punc))
    return no_punc_result.strip()

def remove_punc(string_has_punc):
    no_punc_result = re.sub('[-=+–,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\r\n\t]', '', str(string_has_punc))
    return no_punc_result.strip()

def remove_garbage(string_has_punc): ## Leaves . so that we can recognize sentences

    newline = string_has_punc.replace("\r\n\r\n", " ")
    # print(newline)
    no_punc_result = re.sub('[\r\n\t]', ' ', str(newline))
    return no_punc_result.strip()
    # return newline

def getAllWords(string):
    dict = {}
    processed_list = remove_punc(string).split(" ")
    for word in processed_list:
        dict[word] = 0
#     print(list(dict.keys()))
    return removeSpaceArray(list(dict.keys()))

def getSentences(content):
    retList = []
    for s in tokenize.sent_tokenize(content):
        retList.append(re.sub('[.?!]', ' ', str(s)).strip())
    return retList

def TFIDFSentenceWords(wordList, sentence, IDF1, sentences):
    TFIDFdict = {}
    sList = sentence.split(" ")
    for w in wordList:
        IDF2 = getAppear(w, sentences)
        TF1 = sList.count(w)
        TF2 = len(sList)
        TFIDFdict[w] = (((TF1/TF2)*(1-0.01))+0.01)*np.log((IDF1/(IDF2+1))+1)
    # print(df)
    return TFIDFdict

def getAppear(query, sentences):
    count = 0
    for q in query.split(" "):
        for s in sentences:
            if s.split(" ").count(q) != 0:
                count += 1
                continue
    return count

def queryWordInWords(query, wordList):
    retList = []
    for q in query.split(" "):
        if q in wordList:
            retList.append(q)
    return retList

# doc is the entire document as a string
def getCosine(query, doc):
    cosineList = []
    docNoPunc = remove_punc(doc)
#         print(wordList)
    numSentences = getNumSentences(doc)
    sentences = getSentences(doc)
    largest = 0
    second_largest = 0
    
    for sentence in sentences:
        wordList = getAllWords(sentence) # All the words in the current document
        queryWordsinSentence = queryWordInWords(query, wordList) # query words that are in the sentence words
        TFIDFWords = TFIDFSentenceWords(wordList, doc, numSentences, sentences)
        # print("*****************************************")
        # print(TFIDFWords)
        # print("*****************************************")
        ### Top
        top = 0
        for w in queryWordsinSentence:
            # print("*****************************************")
            # print(w)
            # print("*****************************************")
            top += TFIDFWords[w]
            
            # print(sentence)
                # print(TFIDFWords.keys())
        # if top == 0:
        #     print("*****************************************")
        #     print("top: ",top)
        #     print("query: ",query)
        #     print("sentence: ",sentence)
        #     print("queryWords: ",queryWordsinSentence)
        #     for w in queryWordsinSentence:
        #         print(w)
        #         print(TFIDFWords[w])
        #     print("*****************************************")
        ### Bottom Left
        bLeft = np.sqrt(len(query.split(" ")))
        ### Bottom Right
        bRight = 0
        for w in wordList:
            bRight += TFIDFWords[w]**2
        bRight = np.sqrt(bRight)
        cosineList.append((top)/(bLeft*bRight))
    # print("*****************************************")
    # print(cosineList)
    # print("*****************************************")
    if str(len(cosineList)) == "1":
        return 0, -1
    if str(len(cosineList)) == "2":
        # print("returned due to array size of 2")
        return 0, 1
    
    largest = cosineList.index(max(cosineList))  #  biggest float
    # if max(cosineList) == 0:
    #     print("*****************************************")
    #     print(sentences)
    #     print(query)
    #     print(cosineList)
    #     print("*****************************************")
    
    cosineList2 = cosineList[:]
    cosineList2.pop(largest)
    # print("*****************************************")
    # print("cosineLength: ",len(cosineList))
    # print(str(len(cosineList)) == "1")
    # print(len(cosineList) == 1)
    # print(str(len(cosineList)) == "2")
    # print(len(cosineList) == 2)
    # print(cosineList)
    # print(cosineList2)
    # print("*****************************************")
    onlyZero = True
    for c in cosineList2:
        if c != 0:
            onlyZero = False
    # print(cosineList2)
    # print(onlyZero)
    if onlyZero:
        rNum = np.random.randint(len(cosineList), size=1)[0]
        while rNum == largest:
            rNum = np.random.randint(len(cosineList), size=1)[0]
        # print("*****************************************")
        # print("Largest: ",largest)
        # print("rNum: ",rNum)
        # print("*****************************************")
        return largest, rNum

    try:
        # s_large_float = max(cosineList)
        second_largest = cosineList.index(max(cosineList2))  # second biggest float
        
        # if largest == second_largest:
            # print("Largest and second Largest is the same")
            # print("*****************************************")
            # print("cosineLength: ",len(cosineList))
            # # print("doc: ",doc)
            # print("largest: ", largest)
            # print(max(cosineList))
            # print("second_largest: ", second_largest)
            # print(max(cosineList2))
            # print("cosineList: ", cosineList)
            # print("*****************************************")
        
        return largest,second_largest
    except:
        return largest,-1

def titleRemoval(string, title):
    return string.replace(title,"").strip()

def getSnippets(queryN):
    global CR
    query = queryN
    getRelevantResources(query)
    # print(CR)
    sorted = CR.sort_values(by=["Total"], ascending=False)[['content','content_original','title', 'id', 'Total']].head(50)
    # print(sorted)
    firstSentence = []
    secondSentence = []
    for i in range(len(sorted)):
        # print(sorted['content'].iloc[i])
        s1,s2 = getCosine(query, str(sorted['content'].iloc[i]))
        
        sentences = getSentences(str(sorted['content_original'].iloc[i]))
        titleR = False
        if titleR:
            if s2 == -1:
                firstSentence.append(titleRemoval(remove_garbage(sentences[s1]),str(sorted['title'].iloc[i])))
                secondSentence.append("")
            else:
                firstSentence.append(titleRemoval(remove_garbage(sentences[s1]),str(sorted['title'].iloc[i])))
                secondSentence.append(titleRemoval(remove_garbage(sentences[s2]),str(sorted['title'].iloc[i])))
        else:
            if s2 == -1:
                firstSentence.append(remove_garbage(sentences[s1]))
                secondSentence.append("")
            else:
                firstSentence.append(remove_garbage(sentences[s1]))
                secondSentence.append(remove_garbage(sentences[s2]))
        
    sorted["first"] = firstSentence
    sorted["second"] = secondSentence
    
    # print(sorted[['title','first','second']])
    return sorted[['title','first','second']]