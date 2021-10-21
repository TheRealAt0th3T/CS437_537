from os import remove
import pandas as pd
import re, string
import time
import json
from nltk import tokenize
import math
import customStopWordList
import nltk
# nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import numpy as np

# with open('Computed/wiki_dict.json') as json_file:
#     wiki_dict = json.load(json_file)
# wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id','max_occur_words','max_occur_number']]


wiki = pd.DataFrame()
wiki_dict = []

def set(dataframe, dict):
    global wiki, wiki_dict
    wiki = dataframe
    wiki_dict = dict

def lower_case_str(string_to_be_lower_cased):
    lowercase_str_result = str(string_to_be_lower_cased).lower()
    return lowercase_str_result

def remove_punc_dot(string_has_punc):
    no_punc_result = re.sub('[-=+–,#/\?:^$@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'》\r\n\t]', ' ', str(string_has_punc))
    return no_punc_result

def remove_punc(string_has_punc):
    no_punc_result = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》\r\n\t]', ' ', str(string_has_punc))
    return no_punc_result

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

def filter_tokens(str_to_be_filtered):
    stopword_list = customStopWordList.get_custom_sw_list()
    filtered_tokens = ""
    for w in str(str_to_be_filtered).split(" "):
        if w not in stopword_list:
            filtered_tokens += w + " "
    return filtered_tokens
porter = PorterStemmer()
def stem_tokens(str_to_be_stemmed):
    stemmed_str = ""
    for w in str(str_to_be_stemmed).split(" "):
        stemmed_str += porter.stem(w) + " "
    return stemmed_str

def sentenceTF(word, sentences):
    content = []
    wordCounts = []
    sentenceCount = []
    wordCount = 0
    sentence_notprocessed = tokenize.sent_tokenize(sentences)
    sentence = []
    # print(word)
    for s in sentence_notprocessed:
        temp = remove_punc(s)
        sentence.append(removeSpace(temp))
    # print("sentences: ")
    # print(sentence)
    for s in sentence:
        wordCount = 0
        for w in removeSpaceArray(s.split(" ")):
            # print("Word and w")
            # print(w)
            # print('Are the same? ' + str(word==w))
            if word == w:
                wordCount += 1
        content.append(s)
        wordCounts.append(wordCount)
        sentenceCount.append(len(s.split(" ")))
    df2 = pd.DataFrame(content, columns =['content'])
    df2['WordCounts'] = wordCounts
    df2['NumWords'] = sentenceCount
    df2['TF'] = (df2['WordCounts']/df2['NumWords'])
    # print("\n\n\nprint")
    # print(df2)

    return df2

def sentenceIDF(word, WordCounts, sentence):
    # print("sentence:")
    # print(sentence)
    numSentences = getNumSentences(sentence)
    # print("Numsentence:")
    # print(numSentences)
    nw = 0
    
    # print(sentence)
    for WordCount in WordCounts:
        # print(WordCount)
        if int(WordCount) > 0:
            nw += 1
    
    # print("nw : " + str(nw))
    # print("numsentence: " + str(numSentences))
    # print("nw == 0  is " + str(nw == 0))
    # print("idf returns: ")
    # print(math.log2(numSentences/nw))
    # if word == "arabia":
    #     print("\n\n\nIn sentenceIDF")
    #     print("WordCounts: ")
    #     print(WordCounts)
    #     print("nw : " + str(nw))
    #     print(numSentences)
    #     print(nw)
    #     print(math.log2(numSentences/nw))
    if nw == 0:
        return 0
    elif nw == 1 & numSentences == 1:
        return 1
    else:
        return math.log2(numSentences/nw) # idf


def getSentenceTFIDF(word, sentences):
    # sentence = remove_punc(sentence)
#     print(sentenceTF(word, sentence))
    # if word == "arabia":
    #     print(word)
    #     print(sentences)
    #     print(sentenceTF(word, sentences))
    #     print(sentenceTF(word, sentences)['content'])
    #     print(sentenceTF(word, sentences)['WordCounts'])
    #     print("IDF value for " + str(word) + ", " + str(sentences))
    #     print(sentenceIDF(word, sentenceTF(word, sentences)['WordCounts'], sentences))
    #     print("TFIDF OF arabia")
    #     print(sentenceTF(word, sentences)['TF'] * sentenceIDF(word, sentenceTF(word, sentences)['WordCounts'], sentences))
    return sentenceTF(word, sentences)['TF'] * sentenceIDF(word, sentenceTF(word, sentences)['WordCounts'], sentences)

# print (getSentenceTFIDF('morocco', sample))

def getNumSentences(content):
    return len(tokenize.sent_tokenize(content))
def getSentences(content):
    return tokenize.sent_tokenize(content)
query = ""

def setQuery(q):
    global query
    query = q
    
def getAllWords(dataframe, doc_id):
    dict = {}
    global query
    for q in query.split(" "):
        dict[q] = 0
    processed_list = remove_punc(dataframe['content'].iloc[doc_id]).split(" ")
    for word in processed_list:
        dict[word] = 0
#     print(list(dict.keys()))
    return removeSpaceArray(list(dict.keys()))

def TFIDFAllWords(dataframe, words, doc_id): 
    # print("Here are list of words")
    # print(words)
#     print(len(words))
    TFDocuments = pd.DataFrame()
#     print(dataframe['content'].iloc[0])
    count = 0
    first = True
    for word in words:
        if first:
            sentenceID = []
#             print("Mark")
#             print(dataframe['content'].iloc[count])
#             print(getSentenceTFIDF(word, dataframe['content'].iloc[count]))
            # print("NumSentences: " +str(getNumSentences(dataframe['content'].iloc[doc_id])))
            # print(words)
            # print(dataframe['content'].iloc[doc_id])
            for i in range(getNumSentences(dataframe['content'].iloc[doc_id])):
                sentenceID.append(i)
            TFDocuments = pd.DataFrame(sentenceID, columns=['Sentence_ID'])
            first = False
        # print(word)
        # print("Content: "+str(dataframe['content'].iloc[doc_id]))
        TFDocuments[word] = getSentenceTFIDF(word, dataframe['content'].iloc[doc_id])
        # print("\n\n\nTFDOCUMENTS")
        # print(TFDocuments[word])
#         print("Count: " + str(count))
#         count += 1
    return TFDocuments

def secondHalf(dataframe, doc_id):
    words = getAllWords(dataframe, doc_id)
#     words = 
#     print(words)
    NeedsSum = TFIDFAllWords(dataframe, words, doc_id)
#     print(NeedsSum)
    retVals = []
    for sentenceID in range(len(NeedsSum)):
        retVal = 0
        for word in words:
            # print("please")
            # print(NeedsSum[word])
            # if word == "arabia":
            #     print("Arabia")
            #     print(NeedsSum[word])
            #     print(NeedsSum)
            retVal += float(NeedsSum[word].iloc[sentenceID])**2
        retVals.append(math.sqrt(retVal))
    # print("retVals: ")
    # print(retVals)
    return retVals

# AllWordsTest = wiki.iloc[0:10]
# print(AllWordsTest['content'].iloc[0])
# print(secondHalf(AllWordsTest, 0))

def firstHalf(query):
    firsthalf = math.sqrt(len(query.split(" "))*1)
    return float(firsthalf)

# query = "morroco saudi"
# firstHalf(query)

def cosineSimilarity(query, dataframe):
    firstSentence = []
    secondSentence = []
    setQuery(query)
    for doc_id in range(len(dataframe)): # looks at each document
        # print("document_id: ")
        # print(doc_id)
        currentDoc = dataframe.iloc[doc_id]
        wordList = getAllWords(dataframe, doc_id) # All the words in the current document
#         print(wordList)
        TFIDFWords = TFIDFAllWords(dataframe, wordList, doc_id)
#         print(TFIDFWords)
        numSentences = getNumSentences(dataframe['content'].iloc[doc_id])
        sentences = getSentences(dataframe['content'].iloc[doc_id])
#         print(sentences)
        
        
        top = []
        for i in range(numSentences):
            top.append(0)
        
        for sentenceID in range(numSentences):
            for word in removeSpaceArray(query.split(" ")):
#                 print("Length: " +str(len(top)))
#                 print("SentenceID: "+ str(sentenceID))
#                 print("word: " + str(word))
#                 print("TFIDF of sentence number: " + str(sentenceID) +" for word: " + str(word) +":"+ str(TFIDFWords[word].iloc[sentenceID]))
#                 print("NumSentences: "+str(numSentences))

                top[sentenceID] += float(TFIDFWords[word].iloc[sentenceID]) # TFIDF value of word, sentenceID
                
        # Top part is stored as an array of Total TFIDF values(words in query) by sentences
#         print(top)
        firstBottom = firstHalf(query) # This value does not change upon sentences so it will be static
        secondBottom = secondHalf(dataframe, doc_id) # returns an array of every unique words' sqrt(sum(TFIDF(word)^2))
        
        sentenceNum = []
        cosineRank = []
#         print("NumSentences: "+str(numSentences))
        for i in range(numSentences):
            sentenceNum.append(i)
            # print("firstBottom: " + str(firstBottom))
            # print("secondBottom: " + str(secondBottom[i]))

            cosineRank.append(top[i]/(firstBottom*secondBottom[i]))
        
        rank = pd.DataFrame(sentenceNum,columns=['sentence#'])
        rank['cosine'] = cosineRank
        sorted = rank.sort_values(by=["cosine"], ascending=False)
#         print(sorted)
#         print(sorted['sentence#'].iloc[0])
        if numSentences < 2:
            firstSentence.append(int(sorted['sentence#'].iloc[0]))
            secondSentence.append(-1)
        else:
            firstSentence.append(int(sorted['sentence#'].iloc[0]))
            secondSentence.append(int(sorted['sentence#'].iloc[1]))
    dataframe['firstSentenceID'] = firstSentence
    dataframe['secondSentenceID'] = secondSentence
    return dataframe

def getSnippets(query, CRR):
    # print(CRR)
    CosineFinal = cosineSimilarity(query, CRR)
    
    return CosineFinal

# ms = pd.read_csv("morocco_saudi.csv")
# getSnippets("morocco saudi", ms)