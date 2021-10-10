# **************************************************************
#
# This file will contain our custom list of stop words.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************
import nltk
# nltk.download('stopwords')
from nltk.corpus import stopwords

NLTK_stop_words_list = set(stopwords.words('english'))


# Return the custom list
def get_custom_sw_list():
    return NLTK_stop_words_list
