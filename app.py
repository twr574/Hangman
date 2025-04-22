"""A Python-based implementation of Hangman."""

import math
import os
import random
import time
import sys


def printslow(text,speed=0.1):
    """Prints a string slowly (like a typewriter). Lower speeds print faster."""
    for x in text:
        print(x, end=''),
        sys.stdout.flush()
        time.sleep(speed)
    time.sleep(1)


def printword(ans,letters):
    """Prints the part of a word that have been found in game."""
    letter_string = []
    no_left = 0
    for x in range(0,len(ans)):
        if ans[x] in letters:
            letter_string += f'{ans[x]} '
        else:
            no_left += 1
            letter_string += '_ '
    printslow(letter_string)
    return no_left


def printfile(file):
    """Prints a text file (such as the Hangman diagram each turn)."""
    openfile = open(f'{file}.txt','r')
    printfile = openfile.read()
    print('\n\n')
    printslow(printfile,0.001)
    openfile.close()


def playintro(title,hi_score,play):
    """Plays the intro and main menu."""
    printfile(title)
    print('\n\nWelcome to Hangman v1.0!\n')
    print(f'(Hi-score = {hi_score})')
    menu_input = input('\n'
                       'Press ENTER to start. \n'
                       'Type QUIT (or press ALT+F4 at any time) to exit. \n'
                       'Type HELP for rules. \n'
                       'Type CREDITS for credits. \n'
                       '\n').upper()
    match menu_input:
        case '':
            play += 1
        case 'ENTER':
            play += 1
        case 'QUIT':
            play = 0
        case 'EXIT':
            play = 0
        case 'HELP':
            time.sleep(0.5)
            os.system('cls||clear')
            printfile('rules')
            time.sleep(5)
            input('\n\nPress ENTER to return to title screen.')
            os.system('cls||clear')
        case 'RULES':
            time.sleep(0.5)
            os.system('cls||clear')
            printfile('rules')
            time.sleep(5)
            input('\n\nPress ENTER to return to title screen.')
            os.system('cls||clear')
        case 'CREDITS':
            time.sleep(0.5)
            os.system('cls||clear')
            time.sleep(0.2)
            printfile('credits')
            time.sleep(5)
            os.system('cls||clear')
        case 'EASTEREGG':
            time.sleep(0.5)
            os.system('cls||clear')
            time.sleep(0.2)
            printslow(r'''              _,,gg,,_              ''' '\n'
                      r'''           ,a888P88Y888a,           ''' '\n'
                      r'''         ,d"8"8",YY,"8"8"b,         ''' '\n'
                      r'''        d",P'd' d'`b `b`Y,"b,       ''' '\n'
                      r'''      ,P",P',P  8  8  Y,`Y,"Y,      ''' '\n'
                      r'''     ,P ,P' d'  8  8  `b `Y, Y,     ''' '\n'
                      r'''    ,P ,P_,,8ggg8gg8ggg8,,_Y, Y,    ''' '\n'
                      r'''   ,8P"""""""''      ``"""""""Y8,   ''' '\n'
                      r'''   d'/~\    /~\    /~\    /~\  `b   ''' '\n'
                      r'''   8/   \  /   \  /   \  /   \  8   ''' '\n'
                      r'''   8 ,8, \/ ,8, \/ ,8, \/ ,8, \/8   ''' '\n'
                      r'''   8 "Y" /\ "Y" /\ "Y" /\ "Y" /\8   ''' '\n'
                      r'''   8\   /  \   /  \   /  \   /  8   ''' '\n'
                      r'''   8 \_/    \_/    \_/    \_/   8   ''' '\n'
                      r'''   8                            8   ''' '\n'
                      r'''   Y""""YYYaaaa,,,,,,aaaaPPP""""P   ''' '\n'
                      r'''   `b ag,   ``""""""""''   ,ga d'   ''' '\n'
                      r'''    `YP "b,  ,aa,  ,aa,  ,d" YP'    ''' '\n'
                      r'''      "Y,_"Ya,_)8  8(_,aP"_,P"      ''' '\n'
                      r'''        `"Ya_"""    """_aP"'        ''' '\n'
                      r'''           `""YYbbddPP""'           ''' '\n',0.001)
            printslow('Oh U.',0.2)
            time.sleep(3.5)
            os.system('cls||clear')
            play = 1.1
        case _:
            os.system('cls||clear')
    return play


def playgame(play,score,lives,excess_try):
    """The core game loop. Plays a single level of Hangman."""
    # Obtain words list from files
    words = open('words.txt','r')
    words = words.read()
    words = words.split('\n')
    hard_words = open('wordshard.txt','r')
    hard_words = hard_words.read()
    hard_words = hard_words.split('\n')
    harder_words = open('wordsharder.txt','r')
    harder_words = harder_words.read()
    harder_words = harder_words.split('\n')

    # Difficulty setting - force word length
    if score<100 and play == 2:
        difficulty = 0
        while difficulty not in [1,2,3]:
            try:
                difficulty = int(input('\nSelect a difficulty: \n (1) Easy \n (2) Medium \n (3) Hard \n\n'))
            except ValueError:
                pass
    elif score<1000 and play == 2:
        difficulty = 0
        while difficulty not in [1,2,3,4]:
            try:
                difficulty = int(input('\nSelect a difficulty: \n (1) Easy \n (2) Medium \n (3) Hard \n (4) Very Hard\n\n'))
            except ValueError:
                pass
    else:
        play = 2
        difficulty = 0
        while difficulty not in [1,2,3,4,5]:
            try:
                difficulty = int(input('\nSelect a difficulty: \n (1) Easy \n (2) Medium \n (3) Hard \n (4) Very Hard \n (5) Expert\n\n'))
            except ValueError:
                pass

    # Set word pools and create max guess modification matrix
    match difficulty:
        case 1:
            valid_words = words
            max_guesses = [[0,0,0,0,0],[-1,-1,-1,-1,-1],[-2,-2,-2,-2,-2],[-3,-3,-3,-3,-3],[-4,-4,-4,-4,-4]]
            base_guess = 12
        case 2:
            valid_words = words
            max_guesses = [[0,-1,-1,-2,-2],[-1,-1,-2,-2,-2],[-1,-2,-2,-3,-3],[-2,-2,-3,-3,-4],[-2,-3,-3,-4,-4]]
            base_guess = 10
        case 3:
            valid_words = words + hard_words
            max_guesses = [[0,0,0,-1,-1],[0,0,-1,-1,-2],[-1,-1,-1,-2,-2],[-1,-1,-2,-2,-2],[-2,-2,-2,-2,-3]]
            base_guess = 8
        case 4:
            difficulty = 5
            valid_words = words + 2 * hard_words + harder_words
            max_guesses = [[0,0,0,0,-1],[0,0,0,-1,-1],[0,0,-1,-1,-2],[0,-1,-1,-2,-2],[-1,-1,-2,-2,-2]]
            base_guess = 7
        case 5:
            difficulty = 10
            valid_words = 2 * words + 3 * hard_words + 5 * harder_words
            max_guesses = [[0,0,0,0,0],[0,0,0,0,-1],[0,0,0,-1,-1],[0,0,-1,-1,-1],[0,-1,-1,-2,-2]]
            base_guess = 6

    # Modifies max guesses based on current score: 25,63,157,391,...
    scale = 10
    log_scale = 2.5
    if score < scale*log_scale:
        score_mod = 0
    else:
        score_mod = min(math.floor(math.log(score/scale,log_scale)),4)

    max_lengths = {1: 10, 2: 15, 3: 20, 5: 25, 10: 30}
    min_lengths = {1: 5, 2: 4, 3: 4, 5: 4, 20: 4}
    max_length = max_lengths[difficulty]
    min_length = min_lengths[difficulty]

    # Generate a random word based on the pool of valid words.
    valid_words = [x for x in words if len(x)<=max_length and len(x)>=min_length]
    words_no = len(valid_words)
    word_choice = valid_words[random.randint(0,words_no)].upper()

    # Modifies max guesses based on lengths: {4,5},{6,7},{8,9},{10,11},{12+}.
    if len(word_choice) > 11:
        len_mod = 4
    else:
        len_mod = math.floor(len(word_choice)/2) - 2

    if score < scale*log_scale:
        max_guess = base_guess
    else:
        max_guess = base_guess + max_guesses[len_mod][score_mod]

    # Initialising variables: the 'letter_used' init is intended.
    guess_no = 0
    guess = []
    letter_stock = []
    letter_used = 'None'
    complete = 0
    print(f'\nWord has {len(word_choice)} letters.'
          f'\nMaximum number of incorrect guesses is {max_guess}.')

    # User makes guesses and the validity of the guess is checked.
    while guess != word_choice and guess_no < max_guess and complete == 0:
        if guess_no > 0:
            printfile(f'turn{12-max_guess+guess_no}')
        print('\n\n')
        no_left = printword(word_choice,letter_stock)
        print(f'\n\nCurrently used letters: {letter_used}.')
        if guess_no < max_guess - 1:
            guess = input('\nGuess a word or letter...\n')
        else:
            guess = input('\nFINAL GUESS!\n')
        if len(guess) == 1:
            if guess.upper() not in word_choice or guess.upper() in letter_stock:
                guess_no += 1
            letter_stock += guess.upper()
            letter_used = ', '.join(sorted(set(letter_stock)))
            complete = [x for x in word_choice if x not in letter_stock] == []
        else:
            if guess == word_choice:
                complete = 1
            else:
                guess_no += 1

        time.sleep(0.2)

    # Endgame clean-up. Adjusts lives/score etc. before next level.
    if complete:
        print('\n\nCORRECT! \n')
        excess_try += max_guess - guess_no
        score += int(difficulty*(max_guess - guess_no)*math.ceil(no_left))
        if math.log(excess_try/10,10)%1 == 0 or math.log(excess_try/20,10)%1 == 0 or math.log(excess_try/50,10)%1 == 0:
            lives += 1
            print(f'BONUS 1UP!\n\nNo of Lives is now {lives}.\n')
        printslow(f'Score = {score}')
        time.sleep(0.5)
        next_game = input('\n\nContinue (YES/NO)?\n')
        if next_game in ['YES','Y','','1']:
            play = 2
        elif next_game in ['NO','N','0']:
            print('\nGAME OVER!\n')
            os.system('cls||clear')
            play = 1
    else:
        printfile('turn12')
        lives -= 1
        printslow(f'\n\nThe word was {word_choice}\n')
        if lives > 0:
            print(f'\nLives Remaining {lives}\n')
            next_game = input('Continue (YES/NO)?\n')
            if next_game in ['YES','Y','','1']:
                play = 2
            elif next_game in ['NO','N','0']:
                print('\nGAME OVER!\n')
                time.sleep(3)
                os.system('cls||clear')
                play = 1
        else:
            print('\nGAME OVER!\n')
            os.system('cls||clear')
            play = 1

    return (play,score,lives,excess_try)


# Main driver starts here.
score = 0
lives = 3
play = 1
excess_try = 0
try:
    scorefile = open('hiscore.txt','r+')
    hi_score = int(scorefile.read())
except (FileNotFoundError,ValueError):
    scorefile = open('hiscore.txt','w')
    hi_score = int(0)
    scorefile.write(str(hi_score))
    scorefile.close()

while True:
    if int(play) == 1:
        play = playintro('title',hi_score,play)
    elif int(play) == 2:
        (play,score,lives,excess_try) = playgame(play,score,lives,excess_try)
        if score >= hi_score:
            hi_score = score
    else:
        break
