# **************************************************************
#
# This is the main driver python file which initiates the
# search engine program.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************
# 
import json
import pandas as pd
import time

wiki = pd.read_csv("wiki_ultimate.csv")

# print(wiki["content_original"].iloc[0],"end of the line")
# print(wiki["content"].iloc[0].split(" "),"end of the line")
count = 0
def removeSpace(query):
    global count
    if count % 100000 == 0:
        print(count)
    count += 1
    ret = query.split(" ")
    while "" in ret:
        ret.remove("")
    retStr = ""
    for c in ret:
        retStr += c + " "
    return retStr[0:len(retStr)-1]

wiki["content"] = wiki["content"].apply(removeSpace)
print(wiki["content"].iloc[0].split(" "),"end of the line")
wiki.to_csv("wiki_ultimate2.csv")