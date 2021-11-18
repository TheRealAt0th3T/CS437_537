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
import os
import warnings
warnings.simplefilter("ignore")
import textProcessor as TP
import querySuggestion as QS
import candidateResources_Ranking as CRR
import nltk
# nltk.download('wordnet')
# nltk.download('averaged_perceptron_tagger')
import snippets as SNP

# This is our main "method" block that
# initiates our code
ql_dict = []
ql = pd.DataFrame()
wiki_dict = []
wiki = pd.DataFrame()
# wiki_original = pd.DataFrame()

def readql():
    global ql_dict, ql
    start = time.time()
    with open('Computed/ql_dict_trueid.json') as json_file:
        ql_dict = json.load(json_file)
    print("ql_dict loaded")
    ql = pd.read_csv('Computed/ql_ultimate.csv')[['AnonID','session_id','Query',"Query_original",'QueryTime','length', 'id']]
    print("ql loaded")
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s")
def readwiki():
    global wiki_dict, wiki
    start = time.time()
    with open('Computed/wiki_dict.json') as json_file:
        wiki_dict = json.load(json_file)
    print("wiki_dict loaded")
    wiki = pd.read_csv('Computed/wiki_ultimate.csv')[['content','content_original','title','id','max_occur_words','max_occur_number']]
    print("wiki loaded")
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s")
def readAll():
    global ql_dict, ql, wiki_dict, wiki
    start = time.time()
    with open('Computed/ql_dict_trueid.json') as json_file:
        ql_dict = json.load(json_file)
    print("ql_dict loaded")
    ql = pd.read_csv('Computed/ql_ultimate.csv')[['AnonID','session_id','Query',"Query_original",'QueryTime','length', 'id']]
    # ql_original = pd.read_csv('Computed/ql_original.csv')[['AnonID','Query']]
    print("ql loaded")
    with open('Computed/wiki_dict.json') as json_file:
        wiki_dict = json.load(json_file)
    print("wiki_dict loaded")
    wiki = pd.read_csv('Computed/wiki_ultimate.csv')[['content','content_original','title','id','max_occur_words','max_occur_number']]
    print("wiki loaded")
    # wiki_original = pd.read_csv('Computed/wiki_original.csv')[['content','title','id']]
    # print("wiki_original loaded")
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s\n")
def readSample():
    global wiki_dict, wiki
    with open('Computed/wiki_dict_sample.json') as json_file:
        wiki_dict = json.load(json_file)
    print("wiki_dict loaded")
    wiki = pd.read_csv('Computed/wiki_sample.csv')[['content','content_original','title','id','max_occur_words','max_occur_number']]
    print("wiki loaded")
def minusOne(array):
    ret = []
    for a in array:
        ret.append(int(a)-1)
    return ret
def cleanQuery(query):
    cleaned = TP.lower_case_str(query)
    cleaned = TP.remove_punc(cleaned)
    cleaned = TP.removeSpace(cleaned)
    cleaned = TP.filter_tokens(cleaned)
    # Ex) if user types "one", it gets filtered.
    cleaned = TP.lemmatize_tokens(cleaned)
    cleaned = TP.stem_tokens(cleaned)

    return cleaned

def main():
    # start = time.time()
    # with open('Computed/ql_dict_trueid.json') as json_file:
    #     ql_dict = json.load(json_file)
    # ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
    # with open('Computed/wiki_dict.json') as json_file:
    #     wiki_dict = json.load(json_file)
    # wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id','max_occur_words','max_occur_number']]
    print("Do you wanna build a Search Engine~?")
    QS.set(ql, ql_dict)
    CRR.set(wiki, wiki_dict)
    SNP.set(wiki, wiki_dict)
    
    # The message will print asking the user
    # to enter their query to be searched
    # print("Please type your query and press the \'enter\' key.")

    # Gathering the contents entered by the user and
    # casting the input as type string
    # userQueryInput = str(input())

    # print("What would you like to do with your query " + userQueryInput + "?")
    s = 0
    while(s != 4):
        print("Please select a task using numbers [1,2,3,4]:")
        print("\t1) Suggested Queries \n\t2) Candidate Resources/Relevance Ranking \n\t3) Generate Snippets \n\t4) Exit")
        try:
            s = int(input())
            if s != 4:
                print("Please type your Query:")
                TrueInput = input()
                Uinput = cleanQuery(TrueInput)

            if s == 1:
                print("--------------------------------------------------------------------------------------------------")
                print("Suggested Queries for: \"" + TrueInput + "\"")
                result = QS.filterScores(Uinput)
                for q in result['Query_original'].iloc[0:9].tolist():
                    print("\t" + str(q))
                print("--------------------------------------------------------------------------------------------------")
                # function call
            elif s == 2:
                print("--------------------------------------------------------------------------------------------------")
                print("Calculating Candidate Resources/Relevance Ranking for: \"" + TrueInput + "\"")
                result = CRR.getRelevantResources(Uinput).sort_values(by=["Total"], ascending=False)[['content_original', 'title', 'id', 'Total']]
                print(result[['title','Total']].head(50))
                print("--------------------------------------------------------------------------------------------------")
                print("\n")
                print("Dataframe")
                print(result)
                # function call
            elif s == 3:
                print("--------------------------------------------------------------------------------------------------")
                print("Generating Snippets for: \"" + TrueInput + "\"")
                # print(Uinput)
                # SNP.getRelevantResources(Uinput)
                df = SNP.getSnippets(Uinput)
                # print(df["second"])
                for i in range(len(df)):
                    print("--------------------------------------------------------------------------------------------------")
                    print("(title)\t\t"+str(df["title"].iloc[i]) + "\n")
                    print("(1)\t",df["first"].iloc[i])
                    # print("\n")
                    print("(2)\t",df["second"].iloc[i])
                print("--------------------------------------------------------------------------------------------------")

                print("\n")
                # function call
            elif s == 4:
                print("Okay, Bye...")
                file = "Okay_bye.mp3"
                os.system("afplay " + file)
        except Exception as e: 
            print(e)
            print("Invalid option selected please try again.")

print('Booting the program ...')
# readAll()
readwiki()
# readql()
# readSample()
main()


    # WE CAN JUST REMOVE THE COMMENTS BELOW ONCE EVERYTHING IS WORKING

    # Function to manage query suggestion by the user after the first
    # query has been typed by the user
    # def option_manager(option_input_from_user):
    #     options = {
    #         1: "\nfirst option selected",
    #         2: "\nsecond option selected",
    #         3: "\nthird option selected",
    #         4: "\nfourth option selected",
    #         5: "\nfifth option selected",
    #     }
    # If option '1' or '2' or '3' or '4' or '5' is not selected, then the next
    # line of code will display an invalid message
    # by default.
    #    return options.get(option_input_from_user, "\nInvalid query suggestion selected. Please try again.")

    # Now we ask the user to select a query suggestion option
    # by typing 1, 2, 3, 4, or 5
    # **print("Please select a query option by typing \'1\' or \'2\' or \'3\' or \'4\' or \'5\'")

    # Gathering the option selected by the user and
    # casting the input as type int
    # **userSelectionOption = int(input())

    # the user option is processed and will return what is associated with the option selected.
    # **print(option_manager(userSelectionOption))

    # Used for testing purposes. Once testing is finished with this method, comment it and uncomment the previous
    # lines that are commented with the **
    # tp.print_result()
