# **************************************************************
#
# This is the text processor python file which will process the text in the
# csv file, utilize stop words, stem.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************

import pandas as pd
import customStopWordList
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
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


# This function is used for testing to print the output of the string. It is called in mainDrive.py.
# It is used to see if we are processing the string correctly.
def print_result():
    return print(new_final_str2)


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


# This function removes unnecessary punctuation
def remove_punc(string_has_punc):
    no_punc_result = word_tokenize(re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', ' ', string_has_punc))
    return no_punc_result


# This function will remove words that match the words in the customStopWordList.py
# The function will return reasonable words to index from.
def filter_tokens(str_to_be_filtered):
    stopword_list = customStopWordList.get_custom_sw_list()
    filtered_tokens = []
    for w in str_to_be_filtered:
        if w not in stopword_list:
            filtered_tokens.append(w)
    return filtered_tokens


# Function will stem the tokens. Meaning, it will streamline commoner grammatically structured
# endings from words. Will return a stemmed string/tokens
def stem_tokens(str_to_be_stemmed):
    porter = PorterStemmer()
    stemmed_str = [porter.stem(word) for word in str_to_be_stemmed]
    return stemmed_str


# This function will create an inverted index***********needs to be fixed
def create_inverted_index(str_to_be_inverted):
    inverted_dict = {}
    inverted_list = []

    for w in str_to_be_inverted:
        if w not in inverted_dict:
            inverted_dict[w] = '1'
        elif w in inverted_dict:
            inverted_dict[w] += ',1'
        inverted_list.append((w, '1'))
    return inverted_dict


# testing lower case method
testing_str = lower_case_str(s_test)

# testing remove punctuation
testing_str = remove_punc(testing_str)

# testing removal of stop words
new_final_str = filter_tokens(testing_str)

# testing stemming the tokens
new_final_str = stem_tokens(new_final_str)

# testing creating the index
new_final_str2 = create_inverted_index(new_final_str)
