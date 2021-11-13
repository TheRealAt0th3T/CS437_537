
import pandas as pd
import re, string
import time
import json
import math

with open('ql_ab_dict.json') as json_file:
    ql = json.load(json_file)

for key in ql.keys(): # key is the shortened word
    words = str(ql[key]).split(",")
    filtered = ""
    first = True
    for word in words:
        if key in word:
            if first:
                filtered = word
                first= False
            else:
                filtered += "," + word
    ql[key] = filtered

with open("ql_ab_dict_filtered.json", "w") as f:
    json.dump(ql, f)

# word = 'saudi'
# list = 'saudi,wear,the,consulate,to,in,of,saudis,women,united,religion,and'.split(",")
# compare1 = 'saudi'
# compare2 = 'saudis'
# if word in compare2:
#     print("Good")


