import json
import os
import pyinputplus as pyint
import logging

# idea for the database was found at https://github.com/snori74/twenty

logging.basicConfig( level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable()
logging.debug( '============Program start=============' )

# function that asks the user for the category
def whichCategory():
    print('Welcome to the game of 20 questions.')
    while True:
        userInput = input('Which category would you like to choose? |animals - vegitables - minerals| ')
        if userInput.lower() == 'animals':
            category = 'animals'
            break
        if userInput.lower() == 'vegitables':
            category = 'vegitables'
            break
        if userInput.lower() == 'minerals':
            category = 'minerals'
            break
        else:
            print('Please enter one of the choices.')
    return category

# function that will load the file based on the category, if there is no current file the game will create a file for that category.
def loadFile(category):
    question = {}
    try:
        qFile = open(category + '20q.txt')
        question = json.load(qFile)
    except IOError:
        print(f'You currently dont have a file for the {category}. A file is being created for {category}. ')
        open(category + '20q.txt', "x")
        if category == 'animals':
            question['1'] = [ 'Does your animal meow?', 'cat', 'dog']
        if category == 'vegitables':
            question['1'] = [ 'is your vegitable orange?', 'carrot', 'brocolli']
        if category == 'minerals':
            question['1'] = [ 'is your mineral clear', 'diamnond', 'gold' ]
    return question

# function to ask the user for yes or no question 
def yesNo():
    while True:
        userInput = pyint.inputYesNo(' Answer Yes or No - ') 
        if userInput == 'yes':
            break
        if userInput == 'no':
            break
        else:
            print('please respond with a Y or a N.')
    return userInput

# function that asks the user if they would like to play again
def again():
    print('Would you like to play again?')
    userInput = yesNo()
    if userInput == 'yes':
        playAgain = True
    else:
        playAgain = False
    return playAgain

playAgain = True

# Game Logic
# loop that plays as long as the user wants to play again
while playAgain:
    # check which category the user wants
    category = whichCategory()
    #loads the questions depending on the category
    question = loadFile(category)

    currentQuest = 1
    questions = 0
    # begin asking questions and gather yes or no input and add one to the amount of questions asked
    while True:
        logging.debug( f'current category questions and branchs {question}' )
        logging.debug( f'current question and branchs {question[str(currentQuest)]}' )
        questions = questions + 1
        print(question[str(currentQuest)][0])
        userInput = yesNo()
        # determine the branch taken from the users answer to the yes and no question
        if userInput =='yes':
            branch = 1
        else:
            branch = 2

        # if statement that will check if the current branch leads to a string
        if isinstance (question[str(currentQuest)][branch], str):
            logging.debug( f'current answer {question[str(currentQuest)][branch]}' )
            
            # checks with the user if the category item the database has is their category item
            print(f'Is your {category.replace("s","")} a {question[str(currentQuest)][branch]}?')
            userInput = yesNo()
            # if it is there category item they will be told how many questions it took to get to their category item
            if userInput == 'yes':
                print(f'Your {category.replace("s","")} was guessed in {questions} questions!')
                
                # asks if the user would like to play again
                playAgain = again()
                break
            # else the program will begin to find what the users category item is and get a question for the item
            else:          
                # gets the new category item from the user and checks if the input has only letters and spaces within it
                # the code for checking if there is only letters and spaces, I found at https://stackoverflow.com/questions/29460405/checking-if-string-is-only-letters-and-spaces-python
                while True:
                    userAns = input(f'if {question[str(currentQuest)][branch]} is not your {category.replace("s","")} then what is? ')
                    if all(x.isalpha() or x.isspace() for x in userAns):
                        break
                    else:
                        print("Please enter no numbers or special characters.")

                # gather a new question from the user that will conclude with their animal
                userQuest = input(f'Give me a question that will conclude with your {category.replace("s","")}. ')
                
                logging.debug( f'current length of dictionary {len(question)}' )
                
                # add new question to the dictionary
                question[len(question) + 1] = [userQuest, userAns.lower(), question[str(currentQuest)][branch]]
                
                # update the old branch with the new question number
                question[str(currentQuest)][branch] = len(question)

                # update the text database with the new information
                with open (category + '20q.txt', 'w') as outfile:
                    json.dump(question, outfile)

                # check if the user would like to play again
                playAgain = again()
                break
            
        else:
            # Use the int from the branch to change the current question 
            logging.debug( f'number of next question {question[str(currentQuest)][branch]}' )
            currentQuest = question[str(currentQuest)][branch]

print("Thanks for playing!!!")

            
logging.debug( '============Program end=============' )
        