# -*- coding: utf-8 -*-
"""
Created on Sat May  9 20:42:18 2020

@author: Matheus Ruggeri
"""

import pygame.gfxdraw
import pygame
import csv
import random
import sys
import os.path

# Number of lines, columns and connections Connect4 -> k = 4
nlin = 6
ncol = 7
k = 4

lig4_board = [["m"]*(ncol+2) for i in range(nlin+2)]

# The possible values to the board
EMPTY = ' '
FRAME = 'm'
PLAYER1 = ['X', 'YOU']
PLAYER2 = ['O', 'YOU']

# All the colors and the Radius of the pieces
# The radius should be 32, but every software has a different way to implement circles in to pixels (squares)
# This +2 in the radius will ensure that there will be no background pixel where it should be
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
GOLD = (212, 175, 55)
RADIUS = 32+2


# This function will help the program to know where the plot starts
def xPosition(column): 
    return column * 96 + 48


# This function will help the program to know where the plot starts
def yPosition(line): 
    return line * 88 + 44


# To the click function you need the oposite, get the click position and find the column number
def column(xPosition): 
    return round((xPosition - 48) / (96))


# This is the board size
sizeX = 96*(ncol+2)
sizeY = 88*(nlin+2)

# The lastLine is the line of the last piece, fall is the speed of the fall (has to be a 64 divisor), word is the translation
lastLine = 0
fall = 11
words = None

# Initiate the pygame, the font, display and clock
pygame.init()
win = pygame.display.set_mode((sizeX, sizeY))
clock = pygame.time.Clock()
clock.tick(60)
pygame.display.set_caption("Connect4")
BIG = pygame.font.SysFont("Verdana", 40)
SMALL = pygame.font.SysFont("Verdana", 20)
crash_sound = pygame.mixer.Sound("sounds/crash.ogg")


class flag(object):
    def __init__(self, x, y, initials):
        self.x = x
        self.y = y
        self.img = pygame.image.load("img/"+initials+".png").convert_alpha()
        
    def draw(self, screen):
        self.screen = screen
        screen.blit(self.img, pygame.rect.Rect(self.x, self.y, 64, 64))


class meme(object):
    def __init__(self, x, y, difficult):
        self.x = x
        self.y = y
        self.img = pygame.image.load("img/"+difficult+".png").convert_alpha()
        
    def draw(self, screen):
        self.screen = screen
        screen.blit(self.img, pygame.rect.Rect(self.x, self.y, 64, 64))


class tiled_board(object):
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.img = pygame.image.load("img/"+num+".png").convert_alpha()
        
    def draw(self, screen):
        self.screen = screen
        screen.blit(self.img, pygame.rect.Rect(self.x, self.y, 64, 64))            


class ball(object):
    def __init__(self, x, y, color, isfalling):
        self.x = x
        self.y = y
        self.color = color
        self.isfalling = isfalling
        
    def draw(self, win):
        if (self.isfalling):
            nDisloc = 0
            while (nDisloc < self.y):
                nDisloc += fall
                pygame.draw.rect(win, BLACK, ((self.x-RADIUS), (nDisloc-RADIUS-fall-1), 2*RADIUS, 2*RADIUS+fall))   
                pygame.draw.circle(win, self.color, (self.x, nDisloc), RADIUS)
                draw_board(win, column(self.x))
                pygame.display.update()
            pygame.mixer.Sound.play(crash_sound)
            pygame.time.wait(1)
            self.isfalling = False


class star(object):
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        
    def draw(self, screen):
        self.screen = screen
        x = self.x - 27
        y = self.y - 27
        pygame.draw.polygon(screen, self.color, ((x+26, y+0), (x+32.4, y+19), (x+52.4, y+19), (x+36.2, y+30.8),
                                                 (x+42.4, y+49.8), (x+26.2, y+38), (x+10, y+49.8), (x+16.2, y+30.8), (x+0, y+19), (x+20, y+19)))


def main():
    vez = ""
    finished = False
    # Starts the board
    start_board(lig4_board)
    win.fill(BLACK)
    pieces = {1: ball(0, 0, BLACK, False)}
    ballN = 2
    draw_board(win, 0) 
    # Keep running until there is a return
    while (not finished):
        # Change the next player
        difficult = PLAYER2[1] if (vez == PLAYER1[0]) else PLAYER1[1]
        vez = PLAYER2[0] if (vez == PLAYER1[0]) else PLAYER1[0]
        # Get the color for the next player
        color = RED if (vez == PLAYER1[0]) else BLUE
        played = False
        while (played == False):
            # If the player is a human wait until a column is selected:
            if (((vez == PLAYER1[0] and PLAYER1[1] == "YOU") or (vez == PLAYER2[0] and PLAYER2[1] == "YOU")) and played == False):
                for event in pygame.event.get():
                    # If the mouse was clicked, pass the position to the function that calculates the column
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        colNum = column(event.pos[0])
                        # If the position is not valid (click outside of the window) keep waiting for a click
                        if (int(colNum) < 1 or int(colNum) > ncol):
                            break
                        # If it is possible to make the selected moviment, do it, else, wait for a new one
                        elif (play(lig4_board, colNum, vez) == True):
                            played = True
                    elif event.type == pygame.QUIT:
                        quit_game()
            # If the player is a computer, asks for the AI:
            elif (played == False):
                colNum = AI(lig4_board, difficult, vez)
                if (play(lig4_board, colNum, vez) == True):
                    played = True
        
        # Prints the board in the Terminal/CMD
        print_board(lig4_board)
        # Creates a new objected called Ball that is gonna be printed
        pieces.update({ballN: ball(xPosition(colNum), yPosition(lastLine), color, True)})
        ballN += 1
        # Draw the objects in the dict and Update the display (it is important to all show the new images)
        for (ID, obj) in pieces.items():
            obj.draw(win)
        pygame.display.update()
        # Count the number of connected pieces and check for a full board
        if (count_connections(lig4_board, colNum)[0] >= k or check_full_board(lig4_board) == True):
            # If there is a winner, print it, else, the board is full, then return zero
            if count_connections(lig4_board, colNum)[0] >= k:
                colorText = "RED" if (color == RED) else "BLUE"
                # Print the stars
                print_winner_move(win, lig4_board, count_connections(lig4_board, colNum)[1])
                # Print the information in Terminal, them print in the screen
                print(words["Winner-"+lang] + " " + colorText)
                if colorText == "RED":
                    text_write(words["Winner-"+lang] + "\n" + words["Red-"+lang], RED, "CENTER", BIG, win, True, True, False)
                elif colorText == "BLUE":
                    text_write(words["Winner-"+lang] + "\n" + words["Blue-"+lang], BLUE, "CENTER", BIG, win, True, True, False)
            else:
                # Print the information in Terminal, them print in the screen
                print(words["Draw-"+lang])
                text_write(words["Draw-"+lang], GOLD, "CENTER", BIG, win, True, True, False)
            finished = True
            pygame.time.wait(2500)
            return play_again()


# Starts the board putting a FRAME in all the sites and EMPTY value inside
def start_board(lig4_board):
    for i in range(0, nlin+2):
        lig4_board[i][0] = FRAME
        lig4_board[i][ncol+1] = FRAME
    for j in range(0, ncol+2):
        lig4_board[0][j] = FRAME
        lig4_board[nlin+1][j] = FRAME
    for i in range(1, nlin+1):
        for j in range(1, ncol+1):
            lig4_board[i][j] = EMPTY
    boardN = 0
    for i in range(0, nlin+2):
        for j in range(0, ncol+2):
            boardN += 1
            if lig4_board[i][j] != FRAME:
                img = "1"
            elif lig4_board[i][j] == FRAME:
                if i == 0 and j == 0:
                    img = "2"
                elif i == nlin+1 and j == 0:
                    img = "8"
                elif i == 0 and j == ncol+1:
                    img = "4"
                elif i == nlin+1 and j == ncol+1:
                    img = "6"
                elif i == 0:
                    img = "3"
                elif j == 0:
                    img = "9"
                elif i == nlin+1:
                    img = "7"
                elif j == ncol+1:
                    img = "5"
                else:
                    img = "10"
            board.update({boardN: tiled_board(96*j, 88*i, img)})


# Draw the board in pygame
def draw_board(window, column):
    column += 1
    columnUpdate = list(range(column, (ncol+2)*(nlin+1), ncol+2))
    # If is the first time, prints all the tiles
    if column == 1:
        for (ID, obj) in board.items():
            obj.draw(window)
    # For performance sake, it will only redraw the column selected
    else:
        for (ID, obj) in board.items():
            if ID in columnUpdate:
                obj.draw(window)
    
    pygame.display.update()
    
    
# Prints the board in the Terminal/CMD
def print_board(lig4_board): 
    i = 1
    j = 0
    lin = 1
    col = 1
    while (i < nlin+1):
        print("   ", end='')
        for j in range(1, ncol+1):
            print("+---", end='')
        print("+")
        print(" " + str(lin), end=' ')
        lin += 1
        for j in range(1, ncol+1):
            print("| " + lig4_board[i][j], end=' ')
        i += 1
        print("|\n", end='')
    if (i == nlin+1):
        print("   ", end='+')
        for j in range(1, ncol+1):
            print("---+", end='')
        print("\n     ", end='')
        for j in range(1, ncol+1):
            print(str(col), end='   ')
            col += 1
    print("")


# Calculate the x and y position for the images
def img_pos_calculation(n, width, margin=25):
    screen_width, screen_height = pygame.display.get_surface().get_size()
    extraSpace = screen_width - margin * (n-1) - n * width
    xPos = []
    yPos = ((screen_height - width)/2)
    for i in range(0, n):
        xPos.append(extraSpace/2 + i * (width + margin))
    return xPos, yPos


# In this function you select the language, draw the 3 flags and wait for a click
def select_language():
    langImport = False
    file = "data/lang.cfg"
    if os.path.isfile(file):
        f = open(file, "r")
        initials = f.read()
        if initials == "BR" or initials == "EN" or initials == "DE":
            langImport = True
            
    if not langImport:
        select = False
        xPos, yPos = img_pos_calculation(3, 200, 25)
        flags = {1: flag(xPos[0], yPos, "BR")}
        flags.update({2: flag(xPos[1], yPos, "EN")})
        flags.update({3: flag(xPos[2], yPos, "DE")})
        win.fill(GRAY)
        
        text_write("Choose the language", WHITE, "UP", BIG, win, False, False, False)
        for (ID, obj) in flags.items():
            obj.draw(win)
        pygame.display.update()
        while not select:
            x, y = pygame.mouse.get_pos()
            text = " "
            if y >= yPos and y <= yPos+150:
                if x >= xPos[0] and x <= xPos[0]+200:
                    text = "Brazilian"
                    initials = "BR"
                elif x >= xPos[1] and x <= xPos[1]+200:
                    text = "English"
                    initials = "EN"
                elif x >= xPos[2] and x <= xPos[2]+200:
                    text = "German"
                    initials = "DE"
            text_write(text, WHITE, "DOWN", BIG, win, False, False, GRAY)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and text != " ":
                    select = True
                    f = open(file, "w")
                    f.write(initials)
                    f.close()
                elif event.type == pygame.QUIT:
                    quit_game()
    return initials


# In this function you select the players (1 and 2), this shows you all the options, check for a click, draw a golden rect anda wait .5s to avoid double click
def select_player(n):
    select = False
    xPos, yPos = img_pos_calculation(4, 150, 25)
    opponents = {1: meme(xPos[0], yPos, "you")}
    opponents.update({2: meme(xPos[1], yPos, "easy")})
    opponents.update({3: meme(xPos[2], yPos, "normal")})
    opponents.update({4: meme(xPos[3], yPos, "hard")})
    win.fill(GRAY)
      
    text_write(words["CPlayer-"+lang] + " " + str(n), WHITE, "UP", BIG, win, False, False, False)
    for (ID, obj) in opponents.items():
        obj.draw(win)
    pygame.display.update()
    while not select:
        x, y = pygame.mouse.get_pos()
        text = " "
        if y >= yPos and y <= yPos+150:
            if x >= xPos[0] and x <= xPos[0]+150:
                text = words["You-"+lang]
                initials = "YOU"
                edge = xPos[0]
            if x >= xPos[1] and x <= xPos[1]+150:
                text = words["PCEasy-"+lang]
                initials = "EASY"
                edge = xPos[1]
            if x >= xPos[2] and x <= xPos[2]+150:
                text = words["PCMedium-"+lang]
                initials = "MEDIUM"
                edge = xPos[2]
            if x >= xPos[3] and x <= xPos[3]+150:
                text = words["PCHard-"+lang]
                initials = "HARD"
                edge = xPos[3]
        text_write(text, WHITE, "DOWN", BIG, win, False, False, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and text != " ":
                pygame.draw.rect(win, GOLD, ((edge, yPos), (150, 150)), 5)
                pygame.display.update()
                pygame.time.wait(500)
                return initials
            elif event.type == pygame.QUIT:
                quit_game()


# Asks for the user if the game shoud be played again, without modification, with config modification or just quit
def play_again():
    select = False
    xPos, yPos = img_pos_calculation(3, 150, 25)
    again = {1: meme(xPos[0], yPos, "again")}
    again.update({2: meme(xPos[1], yPos, "change")})
    again.update({3: meme(xPos[2], yPos, "no")})
    win.fill(GRAY)

    text_write(words["PAgain-"+lang], WHITE, "UP", BIG, win, False, False, False)
    for (ID, obj) in again.items():
        obj.draw(win)
    pygame.display.update()
    while not select:
        x, y = pygame.mouse.get_pos()
        text = " "
        if y >= yPos and y <= yPos+150:
            if x >= xPos[0] and x <= xPos[0]+150:
                text = words["Same-"+lang]
                initials = "SAME"
            elif x >= xPos[1] and x <= xPos[1]+150:
                text = words["Change-"+lang]
                initials = "CHANGE"
            elif x >= xPos[2] and x <= xPos[2]+150:
                text = words["No-"+lang]
                initials = "NO"
        text_write(text, WHITE, "DOWN", BIG, win, False, False, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and text != " ":
                pygame.display.update()
                pygame.time.wait(500)
                return initials
            elif event.type == pygame.QUIT:
                quit_game()
    
    
# Print the text with selected color. Y can be the position, "UP", "CENTER" or "DOWN". 
# If backRect is True, prints an alpha gray rect. If outline is True, prints a White outline in the text. 
# If erase, prints a rect erasing the ENTIRE line
def text_write(text, color, y, font, window, backRect, outline, erase):
    textBreak = text.splitlines()
    for line in textBreak:
        # Calculate the size of the line and the screen's size
        my_text = font.render(line, 1, BLACK)
        text_width = my_text.get_width()
        text_height = my_text.get_height()
        screen_width, screen_height = pygame.display.get_surface().get_size()
        
        # Get the X position and the y position (if y is a string)
        center_x = (screen_width-text_width)/2
        if y == "CENTER":
            y = (screen_height-text_height)/2
        elif y == "UP":
            y = (screen_height * 0.2)
        elif y == "DOWN":
            y = (screen_height * 0.7)
        
        if backRect:
            window.set_alpha(128) 
            pygame.gfxdraw.box(window, pygame.Rect(center_x-5, y-5, text_width+10, text_height+10), (100, 100, 100, 220))
        
        if erase != False and line != None:
            pygame.gfxdraw.box(window, pygame.Rect(0, y-5, screen_width, text_height+10), erase)
            
        if outline:
            textOutline = font.render(line, True, WHITE)
            window.blit(textOutline, (center_x + 1, y + 1))
            window.blit(textOutline, (center_x + 1, y - 1))
            window.blit(textOutline, (center_x - 1, y + 1))
            window.blit(textOutline, (center_x - 1, y - 1))

        word_surface = font.render(line, True, color)
        word_width, word_height = word_surface.get_size()
        window.blit(word_surface, (center_x, y))
        y += word_height
        
    pygame.display.update()


# Check if the board is full
def check_full_board(lig4_board):
    j = 1
    cheio = True
    # You are playing this game in a non-flat world with gravity so you only need to check the first line
    while (j <= ncol and cheio == True):
        if (lig4_board[1][j] == EMPTY):
            cheio = False
        j += 1
    return cheio


# Get the column and the Player type and check if his moviment is valid, if it is, play.
def play(lig4_board, col, tipo):
    # Usa o valor máximo da linha e vai decrescendo, retorna se foi possível fazer a jogada
    lin = nlin
    global lastLine 
    possible = False
    jogou = False
    if (lig4_board[1][col] == EMPTY):
        possible = True
        while (jogou == False and lin > 0):
            if (lig4_board[lin][col] == EMPTY):
                lig4_board[lin][col] = tipo
                lastLine = lin
                jogou = True
            else:
                lin -= 1
    return possible


# Removes the last piece from a column, it is a function to help the AI
def undo(lig4_board, col):
    # Apaga a última jogada
    for i in range(1, nlin+1):
        if (lig4_board[i][col] != EMPTY):
            lig4_board[i][col] = EMPTY
            return True


# Count how much pieces are connected
def count_connections(lig4_board, coluna):
    lin = 1
    direct = 1
    i = 1
    j = 1
    lig = 1
    maxLig = 1
    leftDown = True
    rightUp = True
    # Find the last piece from a column (since it is checked in all the moviments, you don't need to check all the pieces)
    while (lig4_board[lin][coluna] == FRAME or lig4_board[lin][coluna] == EMPTY):
        lin += 1
    tipo = lig4_board[lin][coluna]
    # Create 2 dict to print the golden star in the end of the game
    connectedBricks = {1: (coluna, lin)}
    winnerLine = {1: (coluna, lin)}
    while (direct <= 4):
        # Check if there is connected pieces in the Right or Up side
        if (rightUp):
            if (lig4_board[lin+i][coluna+j] == tipo):
                lig += 1
                connectedBricks.update({lig: (coluna+j, lin+i)})
            else:
                rightUp = False
        # Check if there is connected pieces in the Left or Down side
        if (leftDown):
            if (lig4_board[lin-i][coluna-j] == tipo):
                lig += 1
                connectedBricks.update({lig: (coluna-j, lin-i)})
            else:
                leftDown = False
        # Check if there is no connected pieces in any side, just go to the next step
        if (not leftDown and not rightUp):
            leftDown = True
            rightUp = True
            direct += 1
            i = 0 
            j = 0
            # If there are more connected pieces than the max required, there is a winner
            if (lig > maxLig):
                maxLig = lig
                # Save the pieces position to print the stars
                for n in connectedBricks:
                    winnerLine.update({n: connectedBricks[n]})
            lig = 1
        # Checks for the diagonal direction 
        if (direct == 1):  # Diag -> \ <-
            i += 1
            j += 1
        # Checks for the diagonal direction 
        if (direct == 2):  # Diag -> / <-
            i -= 1
            j += 1
        # Checks for the column
        if (direct == 3):  # Col  -> | <-
            i += 1
        # Checks for the line
        if (direct == 4):  # Lin  -> - <-
            j += 1
    return maxLig, winnerLine


# The AI function to find the next moviment
def AI(lig4_board, difficult, vez):
    numCol = (len(lig4_board[0])) - 2
    # Get a random moviment
    nextMoviment = random.randint(1, numCol)
    opponent = PLAYER2[0] if (vez == PLAYER1[0]) else PLAYER1[0]
    numLig = 1
    
    # If it is not EASY, it will see if this is a good moviment
    # The logic is made by priority and difficult
    # EASY ->   Just do some random moviment
    # MEDIUM -> 1st = Win, 2nd = Don't let you win
    # HARD ->   1st = Win, 2nd = Don't let you win, [3rd = Find the moviment that most connect pices, 
    #           4th check if this moviment will not help the opponent to win in the next round] 
    if difficult == "MEDIUM" or difficult == "HARD":
        foundMov = False
        
        # If the AI can win, it will do it
        for j in range(1, ncol+1):
            if (play(lig4_board, j, vez) == True):
                if (count_connections(lig4_board, j)[0] >= k):
                    print("AI can win")
                    foundMov = True
                    nextMoviment = j
                undo(lig4_board, j)
                
        # If the AI can't win, but it can avoid the other player to win, it will do it
        if (foundMov == False):
            print("can't win")
            for j in range(1, ncol+1):
                if (play(lig4_board, j, opponent) == True):
                    if (count_connections(lig4_board, j)[0] >= k):
                        print("AI can avoid")
                        foundMov = True
                        nextMoviment = j
                    undo(lig4_board, j)
        
        # If the AI is HARD, it takes some extra steps thinking in the next moviments
        if difficult == "HARD" and foundMov == False:
            
            # It checks the highest possible connections to increase the connected pieces
            # Do it in 2 loops, so, instead of tending to find the first column as the best in a draw situation,
            #    it will find the middle (that is actually the best choice)
            for j in range(int(ncol/2), ncol+1):
                if (play(lig4_board, j, vez) == True):
                    if (count_connections(lig4_board, j)[0] > numLig):
                        numLig = count_connections(lig4_board, j)[0]
                        nextMoviment = j
                    undo(lig4_board, j)
            for j in range(1, int(ncol/2)):
                if (play(lig4_board, j, vez) == True):
                    if (count_connections(lig4_board, j)[0] > numLig):
                        numLig = count_connections(lig4_board, j)[0]
                        nextMoviment = j
                    undo(lig4_board, j)
                       
            # It will also check if his last moviment will not allow you to win in the next round 
            j = nextMoviment
            if (play(lig4_board, j, vez) == True):
                if (play(lig4_board, j, opponent) == True):
                    if (count_connections(lig4_board, j)[0] >= k):
                        print("Bad move!")
                        # The AI find out that this is a bad moviment, it will do a different one (random)
                        nextMoviment = random.randint(1, numCol)
                    else:
                        foundMov = True
                    undo(lig4_board, j)
                undo(lig4_board, j)
        
    # If the difficult is EASY, just return the random moviment
    # If it is not EASY, it will return the best moviment that it found
    return nextMoviment
    

# Print the stars in the winning connected pieces to show the winner moviment
def print_winner_move(window, lig4_board, movement):
    ballN = 1
    winner_mov = {1: ball(0, 0, BLACK, False)}
    for (ID, obj) in movement.items():
        x, y = obj
        ballN += 1
        winner_mov.update({ballN: star(xPosition(x), yPosition(y), GOLD)})
    for (ID, obj) in winner_mov.items():
        obj.draw(window)
    pygame.display.update()


# Import the CSV file with all the translations
def translation():
    with open('data/translation.csv', mode='r') as infile:
        reader = csv.reader(infile)
        words = {rows[0]: rows[1] for rows in reader}
        return words


# Print the thanks, wait 2 seconds and quit
def quit_game():
    win.fill(GRAY)
    global words
    global lang
    # This (and the globals) are needed since it is possible to quit before even select a language, if this happens, just load the english words
    if (words) == None:
        lang = "EN"
        words = translation()
    text_write(words["Thanks-"+lang], WHITE, "UP", BIG, win, False, False, False)
    text_write(words["Name-"+lang] + "\n" + words["Wiki-"+lang] + "\n" + words["Meme-"+lang] +
               "\n" + words["Kenn-"+lang], WHITE, "DOWN", SMALL, win, False, False, False)
    
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit(0)


# Select the language and get the translation
lang = select_language()
words = translation()

board = {0: tiled_board(0, 0, "0")}

game = "NEW"
while (game != "NO"):
    # If the game is the SAME, just ignore the player selection
    if game != "SAME":
        # Select the players
        PLAYER1.pop()
        PLAYER2.pop()
        PLAYER1.append(select_player(1))
        PLAYER2.append(select_player(2))
    
    # If is the SAME, or you just CHANGE CONFIG, play again
    game = main()
quit_game()