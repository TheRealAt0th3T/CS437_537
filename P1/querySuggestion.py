# **************************************************************
#
# This is the text processor python file which will process the text in the
# csv file, utilize stop words, stem.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************
import os
# current_path = os.getcwd()
# print(current_path)
os.chdir("/Users/steven/Desktop/CS437_537/P1")
import pandas as pd
import customStopWordList
import nltk
import re, string

# nltk.download('punkt')
# nltk.download('stopwords')  # divides a text into a list of sentences to build abbreviations words, collocations,
# and words that start sentences.
# nltk.download('wordnet')  # used to find the meanings of words, synonyms, antonym, and more...


# Sentence string to test logic before using large csv file
s_test = 'Old-school musical numbers, feisty princesses, funny sidekicks and a mix of action, comedy and ' \
         'romance come together in Frozen, a Disney animation that works hard to keep everyone happy. '

# testing string outputs
testing_str = ""

# csvFile contains the contents of the file. This path may be different for
# each of us. Either way, it should be in the format of pd.read_csv("filename/path")
def get_csv_file_content():
    csv_file = pd.read_csv("C:/Users/Ale_Mac5/PycharmProjects/CS437_537/project_1_Wiki_sample.csv")
    return csv_file


# This function will lower case capitalization in the string and will return
# a string that is all lower case
def lower_case_str(string_to_be_lower_cased):
    lowercase_str_result = string_to_be_lower_cased.lower()
    return lowercase_str_result

# testing lower case method
testing_strlowercase = lower_case_str(s_test)

# reading query logs
ql = pd.read_table('project_1_AOL_query_log/Clean-Data-01.txt', sep='\t')

# print(ql)
ql = ql.append(pd.read_table('project_1_AOL_query_log/Clean-Data-02.txt', sep='\t'))
ql = ql.append(pd.read_table('project_1_AOL_query_log/Clean-Data-03.txt', sep='\t'))
ql = ql.append(pd.read_table('project_1_AOL_query_log/Clean-Data-04.txt', sep='\t'))
ql = ql.append(pd.read_table('project_1_AOL_query_log/Clean-Data-05.txt', sep='\t'))
print(ql)