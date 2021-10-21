
import pandas as pd
import re, string
import time
import json
import math

ql_o = pd.read_csv("ql_id.csv")[['AnonID','Query','id']]
ql = pd.read_csv("ql.csv")[['AnonID','Query','id']]
dict = {}

for i in range(len(ql)):
    if i % 100000 == 0:
        print(i)
    windex = 0
    for word in str(ql['Query'].iloc[i]).split(" "):
        # print(word)
        if word in dict.keys():#if cleaned word exist in dictionary
            if str(ql_o['Query'].iloc[i]).split(" ")[windex] not in str(dict[word]).split(","): #but the original word is not the same as before
                dict[word] = str(dict[word]) +","+ str(ql_o['Query'].iloc[i]).split(" ")[windex]
        else: # if cleaned word does not exist in dictionary
            # print(windex)
            # print(ql_o['Query'].iloc[i])
            dict[word] = str(ql_o['Query'].iloc[i]).split(" ")[windex]
        windex += 1

with open("ql_ab_dict.json", "w") as f:
    json.dump(dict, f)


# id = []

# def idlabel():
#     for i in range(len(ql)):
#         id.append(i)

# idlabel()
# ql['id'] = id
# ql.to_csv("ql_id.csv")