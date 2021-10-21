# **************************************************************
#
# This is the main driver python file which initiates the
# search engine program.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************
import customStopWordList
import textProcessor as tp  # importing the textProcessor.py to call its methods


# This is our main "method" block that
# initiates our code
if __name__ == "__main__":
    with open('Computed/ql_dict_trueid.json') as json_file:
        ql_dict = json.load(json_file)
    ql = pd.read_csv('Computed/ql.csv')[['AnonID','session_id','Query','QueryTime','length']]
    with open('Computed/wiki_dict.json') as json_file:
        wiki_dict = json.load(json_file)
    wiki = pd.read_csv('Computed/wiki_punc.csv')[['content','title','id','max_occur_words','max_occur_number']]

    # The message will print asking the user
    # to enter their query to be searched
    print("Please type your query and press the \'enter\' key.")

    # Gathering the contents entered by the user and
    # casting the input as type string
    userQueryInput = str(input())

    print("What would you like to do with your query " + userQueryInput + "?")
    print("1) Suggested Queries \n2) Candidate Resources \n3) Relevance Ranking \n4) Generate Snippets")
    s = int(input())

    if s == 1:
        print("Suggested Queries has been selected.")
        # function call
    elif s == 2:
        print("Candidate Resources has been selected")
        # function call
    elif s == 3:
        print("Relevance Ranking has been selected")
        # function call
    elif s == 4:
        print("Generate Snippets")
        # function call
    else:
        print("Invalid option selected please try again.")





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
