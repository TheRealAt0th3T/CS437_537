# **************************************************************
#
# This is the main driver python file which initiates the
# search engine program.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************
import customStopWordList
# import textProcessor as TP  # importing the textProcessor.py to call its methods
import json
import pandas as pd
import time
import os
import textProcessor as TP
import querySuggestion as QS
import candidateResources_Ranking as CRR
import snippets as SNP

# This is our main "method" block that
# initiates our code
ql_dict = []
ql = pd.DataFrame()
wiki_dict = []
wiki = pd.DataFrame()
wiki_original = pd.DataFrame()

def readql():
    global ql_dict, ql
    start = time.time()
    with open('Computed/ql_dict_trueid.json') as json_file:
        ql_dict = json.load(json_file)
    ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s")
def readwiki():
    global wiki_dict, wiki
    start = time.time()
    with open('Computed/wiki_dict.json') as json_file:
        wiki_dict = json.load(json_file)
    wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id','max_occur_words','max_occur_number']]
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s")
def readAll():
    global ql_dict, ql, wiki_dict, wiki, wiki_original
    start = time.time()
    with open('Computed/ql_dict_trueid.json') as json_file:
        ql_dict = json.load(json_file)
    print("ql_dict loaded")
    ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
    print("ql loaded")
    with open('Computed/wiki_dict.json') as json_file:
        wiki_dict = json.load(json_file)
    print("wiki_dict loaded")
    wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id','max_occur_words','max_occur_number']]
    print("wiki loaded")
    wiki_original = pd.read_csv('Computed/wiki_original.csv')[['content','title','id']]
    print("wiki_original loaded")
    end = time.time()
    print("Initialization complete. Time Elapsed: "+str(end - start)[0:4] + "s")

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
    cleaned = TP.stem_tokens(cleaned)

    return cleaned

def main():
    start = time.time()
    # with open('Computed/ql_dict_trueid.json') as json_file:
    #     ql_dict = json.load(json_file)
    # ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
    # with open('Computed/wiki_dict.json') as json_file:
    #     wiki_dict = json.load(json_file)
    # wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id','max_occur_words','max_occur_number']]
    
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
        print("1) Suggested Queries \n2) Candidate Resources/Relevance Ranking \n3) Generate Snippets \n4) exit")
        s = int(input())
        print("Please type your Query:")
        Uinput = input()
        Uinput = cleanQuery(Uinput)

        if s == 1:
            print("Suggested Queries has been selected.")
            result = QS.getScores(Uinput)
            print(result['Query'].iloc[0:9])
            # function call
        elif s == 2:
            print("Candidate Resources/Relevance Ranking has been selected")
            result = CRR.getRelevantResources(Uinput)
            print(result[['title','Total']])
            # function call
        elif s == 3:
            print("Generate Snippets has been selected")
            result = SNP.getSnippets(Uinput, CRR.getRelevantResources(Uinput))
            # print(result)
            
            firstSentence = []
            secondSentence = []
            sentences = []
            # print(wiki_original['content'].iloc[result['id']].tolist())
            for s in wiki_original['content'].iloc[minusOne(result['id'])].tolist():
                sentences.append(SNP.getSentences(s))
            for i in range(len(result)):
                # print(sentences[i])
                # print([result['firstSentenceID'].iloc[i]])
                firstSentence.append(sentences[i][result['firstSentenceID'].iloc[i]])
                if result['secondSentenceID'].iloc[i] != -1:
                    secondSentence.append(str(sentences[i][result['secondSentenceID'].iloc[i]]))
                else:
                    secondSentence.append("")
            # Show = pd.DataFrame(result['title'].tolist(),columns=['title'])
            # Show['snippet'] = firstSentence
            # print(Show)
            titles = result['title'].tolist()
            for i in range(len(titles)):
                print("--------------------------------------------------------------------------------------------------")
                print("\t"+str(titles[i]) + "\n")
                print(firstSentence[i])
                print("\n")
                print(secondSentence[i])
            print("--------------------------------------------------------------------------------------------------")

            print("\n")
            # function call
        elif s == 4:
            print("Okay, Bye...")
            file = "Okay_bye.mp3"
            os.system("afplay " + file)
        else:
            print("Invalid option selected please try again.")

print('Booting the program ...')
readAll()
# readwiki()
# readql()
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
