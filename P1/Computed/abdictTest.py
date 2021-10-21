
import pandas as pd
import re, string
import time
import json
import math


with open('ql_ab_dict_filtered.json') as json_file:
    ql = json.load(json_file)

print("ready")
str = ""
while str != "exit":
    print(ql[input()])

# id = []

# def idlabel():
#     for i in range(len(ql)):
#         id.append(i)

# idlabel()
# ql['id'] = id
# ql.to_csv("ql_id.csv")