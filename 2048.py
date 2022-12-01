import random
import copy
import mysql.connector


#Creating mysql connection
mydb = mysql.connector.connect( host = "localhost", user = "root",password = "1234",database = "2048game")
mycursor = mydb.cursor()
#Create the board size variable
boardsize = 4
# This function will print out the current board
def display():
    # Find out which value is largest
    largest = board[0][0]
    for row in board:
        for element in row:
            if element > largest:
                largest = element
    # Set the max number of spaces needed in the length of the largest value
    numspaces = len(str(largest))
    for row in board:
        currRow = "|"
        for element in row:
            # if the current element is 0, add a space
            if element == 0 :
                currRow += " " * numspaces + "|"
            # if not, we should add the value
            else:
                currRow += (" " * (numspaces - len(str(element)))) + str(element) + "|"
        # print the generated row.
        print(currRow)
    print()

#This function merges one row left
def mergeonerowLEFT(row):
    #Move everything as far to the left as possible
    for j in range(boardsize - 1):
        for i in range(boardsize - 1, 0 , -1):
            #Test if there is an empty space,move over if so
            if row[i - 1] == 0:
                row[i - 1] = row[i]
                row[i] = 0
    '''Merge everything to the left'''
    for i in range(boardsize - 1):
        '''Test if the current value is identical to the one next to it'''
        if row[i] == row[i + 1]:
            row[i] *= 2
            row[i + 1] = 0
    '''Move everything to the left again'''
    for i in range(boardsize - 1, 0 , -1):
        if row[i - 1] == 0:
            row[i - 1] = row[i]
            row[i] = 0
    return row

''' This function merges the whole board to the left'''
def merge_LEFT(currentboard):
    # Merge every row in the board left
    for i in range(boardsize):
        currentboard[i] = mergeonerowLEFT(currentboard[i])
    return currentboard

# This function reverses the order of one row
def reverse(row):
    ''' Add all elements of the row to a new list, in reverse order'''
    new = []
    for i in range(boardsize -1 , -1, -1):
        new.append(row[i])
    return new

# This function merges the whole board right
def merge_RIGHT(currentboard):
    ''' Look at every row in the board'''
    for i in range(boardsize):
        # Reverse the row, merge to the left , then reverse back
        currentboard[i] = reverse(currentboard[i])
        currentboard[i] = mergeonerowLEFT(currentboard[i])
        currentboard[i] = reverse(currentboard[i])
    return currentboard

# This function transposes the whole board
def transpose(currentboard):
    for j in range(boardsize):
        for i in range(j , boardsize):
            if not i == j :
                temp = currentboard[j][i]
                currentboard[j][i] = currentboard[i][j]
                currentboard[i][j] = temp
    return currentboard

''' This function merges the whole board up '''
def merge_UP(currentboard):
    ''' Transposes the whole board, merges it all left, then transpose it back'''

    currentboard  =  transpose(currentboard)
    currentboard = merge_LEFT(currentboard)
    currentboard = transpose(currentboard)
    
    return currentboard

# This function merges the whole board down
def merge_DOWN(currentboard):
    ''' Transposes the whole board, merges it all right, then transpose it back'''

    currentboard = transpose(currentboard)
    currenboard = merge_RIGHT(currentboard)
    currentboard = transpose(currentboard)

    return currentboard

# This function picks a new value for the board
def picknewvalue():
    if random.randint(1 , 8) == 1:
        return 4
    else:
        return 2

# This function adds a value to the board in one of the empty space
def addnewvalue():
    global score
    score += 1
    row_num = random.randint(0, boardsize - 1)
    col_num = random.randint(0, boardsize - 1)

    while not board[row_num][col_num] == 0:
        row_num = random.randint(0, boardsize - 1)
        col_num = random.randint(0 , boardsize - 1)

    board[row_num][col_num] = picknewvalue()

def won():
    for row in board:
        if 2048 in row:
            return True
    return False

def nomoves():
    # Create two copies of the board()
    tempboard1 = copy.deepcopy(board)
    tempboard2 = copy.deepcopy(board)

    tempboard1 = merge_DOWN(tempboard1)
    if tempboard1 == tempboard2:
        tempboard1 = merge_UP(tempboard1)
        if tempboard1 == tempboard2:
            tempboard1 = merge_LEFT(tempboard1)
            if tempboard1 == tempboard2:
                tempboard1 = merge_RIGHT(tempboard1)
                if tempboard1 == tempboard2:
                    return True
    return False    

        
# Create a blank board
board = []
score = 0
for i in range(boardsize):
    row = []
    for j in range(boardsize):
        row.append(0)
    board.append(row)

''' Fill two spots with random values, to start the game'''
num_needed = 2
while num_needed > 0 :
    row_num = random.randint(0 , boardsize - 1)
    col_num = random.randint(0 , boardsize - 1)

    if board[row_num][col_num] == 0:
        board[row_num][col_num] = picknewvalue()
        num_needed -= 1

# STARTING MENU
print('Welcome to 2048! Your goal is to combine values to get the number 2048, by merging the board in different directions. Everytime, you will need to "s" to merge down, "w" to merge up, "a" to merge left and " d" to merge right. \n\n Here is the starting board::')

print("Press 1 for New Player")
print("Press 2 for Existing player")  
choice = int(input())
Name = input('Enter Your Full Name  : ')
if choice == 1:
    SQL = 'Insert into players (name) values(%s)'
    VAL = (Name.title(),)
    mycursor.execute(SQL,VAL)
    mydb.commit()
    print(mycursor.rowcount,"User Registered")
    print("Press 1 for playing")
    option = int(input())
    if option == 1:
        display()       
else:
    print("Press 1 for playing")
    print("Press 2 for seeing your highest score")
    print("Press 3 for seeing the winners")
    option = int(input())
        
    if option == 1:
        display()
    elif option == 2:
        
        SQL = 'Select max(score) from players where name like %s '
        VAL = (Name.title(),)
        mycursor.execute(SQL,VAL)
        result = mycursor.fetchone()
        print('YOUR HIGHEST SCORE:')
        print(result)
        print("Start new round by pressing any key from wasd")
                
    elif option == 3:
        status = "Win"
        SQL = 'Select * from players where status like %s '
        VAL = (status,)
        mycursor.execute(SQL,VAL)
        result = mycursor.fetchall()
        if result == []:
            print("There is no winner yet!")
        else:
            print('WINNERS:')
            for i in result:
                print(i)
        print("Start new round by pressing any key from wasd")

game_over = False
# Repeat asking the user for new moves while the game isn't over
while not game_over :
    print('Your score right now = ', score)
    move  = input("Which way you want to merge?")

    # Assume they entered a valid input
    valid_input = True

    # Create a copy of the board
    tempboard = copy.deepcopy(board)

    ''' Figure out which way the person wants to merge and use the
    correct function'''
    if move == 'w':
        board = merge_UP(board)
    elif move == 's':
        board = merge_DOWN(board)
    elif move == 'd':
        board = merge_RIGHT(board)
    elif move == 'a':
        board = merge_LEFT(board)
    else:
        valid_input = False

    if not valid_input:
        print('Your input was not valid, please try again')
    else:
        if board ==  tempboard:
            print('Try a different direction!')
            end = input("Want to continue or exit(y for exit / any key for continue)")
            if end == "y":
                game_over = True
                SQL = "Insert into players (name,score) values(%s,%s)"
                VAL = (Name.title(),score)
                mycursor.execute(SQL,VAL)
                print('Record updated')
                print("Thank you so much for playing")
                mydb.commit()
                print("Your final score is ", score)
                print("Press 1 for playing")
                print("Press 2 for seeing your highest score")
                print("Press 3 for seeing the winners")
                option = int(input())
                
                if option == 1:
                    display()
                    game_over = False
                elif option == 2:            
                    SQL = 'Select max(score) from players where name like %s '
                    VAL = (Name.title(),)
                    mycursor.execute(SQL,VAL)
                    result = mycursor.fetchone()
                    print('YOUR HIGHEST SCORE:')
                    print(result)
                        
                elif option == 3:
                    status = "Win"
                    SQL = 'Select * from players where status like %s '
                    VAL = (status,)
                    mycursor.execute(SQL,VAL)
                    result = mycursor.fetchall()
                    if result == []:
                        print("There is no winner yet!")
                    else:
                        print('WINNERS:')
                        for i in result:
                            print(i)
                                                       
                
        else:
            # Test if user has won
            if won():
                display()
                status = "Win"
                SQL = "Insert into players (name,score,status) values(%s,%s,%s)"
                VAL = (Name.title(),score,status)
                mycursor.execute(SQL,VAL)
                mydb.commit()
                print("YOU WON!!!!")
                game_over = True
                
            else:
                addnewvalue()
                display()
                # Test if user lost
                if nomoves():
                    status = "Lose"
                    print("SORRY! You have no more possible move, you lose!")
                    SQL = "insert into players (name,score,status) values(%s,%s,%s)"
                    VAL = (Name.title(),score,status)
                    mycursor.execute(SQL,VAL)
                    mydb.commit()
                    print("Your final score is ", score)
                    SQL = "Update players set score = %s where name = %s"
                    VAL = (score,Name.title())
                    mycursor.execute(SQL,VAL)
                    mydb.commit()
                    game_over = True


