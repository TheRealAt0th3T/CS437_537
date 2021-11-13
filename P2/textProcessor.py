import customStopWordList
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re

def lower_case_str(string_to_be_lower_cased):
    lowercase_str_result = str(string_to_be_lower_cased).lower()
    return lowercase_str_result

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