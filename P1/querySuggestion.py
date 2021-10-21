# **************************************************************
#
# Query Suggestion
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************

import pandas as pd
import re, string
import time
import json

# SESSION ID
# Opening .json
# with open('Computed/ql.json') as json_file:
#     ql_dict = json.load(json_file)
# ql = pd.read_csv('Computed/ql.csv')[['AnonID', 'Query', 'QueryTime']]
# print(ql)

# num = 0
# prev_id = 0

# SessionID Function -
# def sessionID(id):
#     global num, prev_id
#     if prev_id != int(id):
#         num = num + 1
#         prev_id = int(id)

#     return num

# ql['session_id'] = ql['AnonID'].apply(sessionID)
# ql = ql[['AnonID','session_id','Query','QueryTime']]
# ql.to_csv('ql.csv')



# QUERY LENGTH
# ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime']]
# print(ql)

# def queryLength(query):
#     ret = query.split(" ")
#     while "" in ret:
#         ret.remove("")
#     return len(ret)


# ql['length'] = ql['Query'].apply(queryLength)
# ql = ql[['AnonID','session_id','Query','QueryTime','length']]
# ql.to_csv('ql.csv')



# QUERY SUGGESTION
# with open('Computed/wiki.json') as json_file:
#     wiki_dict = json.load(json_file)
# wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id']]
# print(wiki)
# start = time.time()

# with open('Computed/ql_dict_trueid.json') as json_file:
#     ql_dict = json.load(json_file)
# ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
# print(ql)
# end = time.time()
# print(end - start)




# GETROWS
# print(wiki_dict['merit'])
# print(wiki_dict['merit'].keys())
# '940', '1167'
ql_dict = []
ql = pd.DataFrame()
def set(dataframe, dict):
    global ql_dict, ql
    ql = dataframe
    ql_dict = dict

# Takes a word, returns all rows of dataframe that contain the word, that has a bigger length than num
def getRows(word, num):
    # print(ql_dict[str(word)].keys()) return ql[(ql['session_id'].astype('str').isin(list(ql_dict[str(word)].keys(
    # )))) & (ql['length'].astype('int64') > num)]
    return ql.iloc[list(ql_dict[str(word)].keys())][ql['length'].astype('int64') > num]

# word = 'vietnam'  # THIS LINE NEEDS TO BE FIXED*********************
# word = word.strip()


# print(len(word.split(" ")))
# print(getRows(word, len(word.split(" "))))
# print(ql[ql['length'].astype('int64') > 2])


def getScores(words):
    result = pd.DataFrame()
    first = True
    numWords = len(words.split(" "))
    for word in words.split(" "):
        Rows = getRows(word, numWords) # n + 1
#         print("Rows " + word)
#         print(Rows) # This prints all rows that contain the row
        if first:
            result = Rows[['session_id','Query','QueryTime']]
            first = False
        else:
            result.append(Rows[['session_id','Query','QueryTime']])
    
#     print(result)
    result = result.groupby(["Query","session_id"]).count().rename(columns={"QueryTime":"Occurance_per_session_id"})
    result = result.reset_index()
    # print(result) # This prints count for a single session
    result = result.groupby(by=['Query']).count().reset_index()
    result['Score'] = result['Occurance_per_session_id']/len(Rows.groupby(by=["session_id"]))
#     print(result)
    
    return result

def filterScores(words):
    result = getScores(words)
#     print(result)
    for i in range(len(result)):
        if result['Query'].iloc[i][0:len(words)] == words:
            result['Score'].iloc[i] += 1
    result = result.sort_values(by=["Score"], ascending=False)[['Query', 'Occurance_per_session_id', 'Score']].reset_index()
    return result
    # print(str(len(Count.groupby(by=["session_id"]))) + " individual sessions")

# print(getScores("peru illinoi"))
# print(filterScores("peru illinoi"))