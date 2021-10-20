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
with open('Computed/ql.json') as json_file:
    ql_dict = json.load(json_file)
ql = pd.read_csv('Computed/ql.csv')[['AnonID', 'Query', 'QueryTime']]
# print(ql)

num = 0
prev_id = 0

# SessionID Function -
def sessionID(id):
    global num, prev_id
    if prev_id != int(id):
        num = num + 1
        prev_id = int(id)

    return num

ql['session_id'] = ql['AnonID'].apply(sessionID)
ql = ql[['AnonID','session_id','Query','QueryTime']]
# ql.to_csv('ql.csv')



# QUERY LENGTH
# ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime']]
# print(ql)

def queryLength(query):
    ret = query.split(" ")
    while "" in ret:
        ret.remove("")
    return len(ret)


ql['length'] = ql['Query'].apply(queryLength)
ql = ql[['AnonID','session_id','Query','QueryTime','length']]
# ql.to_csv('ql.csv')



# QUERY SUGGESTION
# with open('Computed/wiki.json') as json_file:
#     wiki_dict = json.load(json_file)
# wiki = pd.read_csv('Computed/wiki.csv')[['content','title','id']]
# print(wiki)
# start = time.time()

with open('Computed/ql_dict_trueid.json') as json_file:
    ql_dict = json.load(json_file)
ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
# print(ql)
# end = time.time()
# print(end - start)




# GETROWS
# print(wiki_dict['merit'])
# print(wiki_dict['merit'].keys())
# '940', '1167'

# Takes a word, returns all rows of dataframe that contain the word, that has a bigger length than num
def getRows(word, num):
    # print(ql_dict[str(word)].keys()) return ql[(ql['session_id'].astype('str').isin(list(ql_dict[str(word)].keys(
    # )))) & (ql['length'].astype('int64') > num)]
    return ql.iloc[list(ql_dict[str(word)].keys())][ql['length'].astype('int64') > num]

word = 'vietnam'  # THIS LINE NEEDS TO BE FIXED*********************
word = word.strip()


# print(len(word.split(" ")))
# print(getRows(word, len(word.split(" "))))
# print(ql[ql['length'].astype('int64') > 2])

Rows = getRows(word, len(word.split(" ")))
# print(Rows) # This prints all rows that contain the row
result = Rows[['session_id','Query','QueryTime']].groupby(["Query","session_id"]).count().rename(columns={"QueryTime":"Occurance_per_session_id"})
result = result.reset_index()
# print(result) # This prints count for a single session
result = result.groupby(by=['Query']).count()
result['Score'] = result['Occurance_per_session_id']/len(Rows.groupby(by=["session_id"]))
# # print(str(len(Count.groupby(by=["session_id"]))) + " individual sessions")
result = result.sort_values(by=["Score"], ascending=False)[['Occurance_per_session_id', 'Score']]

print(result) # suggested queries output