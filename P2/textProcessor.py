import customStopWordList
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import nltk

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

def get_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)

lemmatizer = WordNetLemmatizer()
def lemmatize_tokens(str_to_be_lemmatized):
    lemmed_str = ""
    for w in str(str_to_be_lemmatized).split(""):
        lemmed_str += lemmatizer.lemmatize(w, get_pos(w)) + " "
    return lemmed_str

porter = PorterStemmer()
def stem_tokens(str_to_be_stemmed):
    stemmed_str = ""
    for w in str(str_to_be_stemmed).split(" "):
        stemmed_str += porter.stem(w) + " "
    return stemmed_str