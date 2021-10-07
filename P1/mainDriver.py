# **************************************************************
#
# This is the main driver python file which initiates the
# search engine program.
#
# AUTHORS: Amara Tariq, Steven Kim, Alejandro Macias
#
# **************************************************************

# Function to manage query suggestion by the user after the first
# query has been typed by the user
def option_manager(option_input_from_user):
    options = {
        1: "\nfirst option selected",
        2: "\nsecond option selected",
        3: "\nthird option selected",
        4: "\nfourth option selected",
        5: "\nfifth option selected",
    }
    # If option '1' or '2' or '3' or '4' or '5' is not selected, then the next
    # line of code will display an invalid message
    # by default.
    return options.get(option_input_from_user, "\nInvalid query suggestion selected. Please try again.")


# This is our main "method" block that
# initiates our code
if __name__ == "__main__":

    # The message will print asking the user
    # to enter their query to be searched
    print("Please type your query and press the \'enter\' key.")

    # Gathering the contents entered by the user and
    # casting the input as type string
    userQueryInput = str(input())

    # Now we ask the user to select a query suggestion option
    # by typing 1, 2, 3, 4, or 5
    print("Please select a query option by typing \'1\' or \'2\' or \'3\' or \'4\' or \'5\'")

    # Gathering the option selected by the user and
    # casting the input as type int
    userSelectionOption = int(input())

    # the user option is processed and will return what is associated with the option selected.
    print(option_manager(userSelectionOption))
