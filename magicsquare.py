import pygame # For GUI

import sqlite3 # For Database

import random # For my magic square

# These are all the libraries i have imported for my game with each one beinhg used for its purpose.

# Below are all startup variables that are used within my code and these also include global variables.
# These global variables are used in different sections of my program.
pygame.init()
width = 600
height = 600
screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Magic Square !")
fps = 60
rows, cols = 8, 8
sizesq = height//rows
pink = (255, 192, 203)
white = (255, 255, 255)
black = (0, 0, 0)
blue = (0, 0, 255)
green = (0,255,0)
timer = pygame.time.Clock()
main_menu = False
ge = False 
mcnt = 0
cnt = 0
cc = 1
rulesy = False
loginP = True
tors = 0
selectedbox = 0
textboxtext1 = ''
textboxtext2 = ''
textboxtext3 = ''
opposition = ''
prev_mouse_state = False
curr_mouse_state = False
scoring = False
currscore = 0
oppscore = 0
datatrack = 0
prev_score = False
all_scores = False
scorepage = False
Police = pygame.transform.scale(pygame.image.load('Sprites/sprite1.png'), (44,25))
Robber = pygame.transform.scale(pygame.image.load('Sprites/Sprite2.png'), (44,25))
font1 = pygame.font.Font('freesansbold.ttf', 18)
font2 = pygame.font.Font('freesansbold.ttf', 12)
font3 = pygame.font.Font('freesansbold.ttf', 13)
font4 = pygame.font.Font('freesansbold.ttf', 6)



#Initialises the database
connection1 = sqlite3.connect('userdata.db')
curr1 = connection1.cursor()

# Creates the table 
curr1.execute('''
CREATE TABLE IF NOT EXISTS userdata( 
    id INTEGER PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
)
''')
# ID uses an integer datatype as it is made up of numerical digits.
# Uses specfic datatype VARCHAR as username and password are both words containing letter characters.

# The variables for the login is placed here and also inserted by calling the cursor
slog, spword = 'Student', 'Studentpass'
tlog, tpword = 'Teacher', 'Teacherpass'

usernamelist = [slog,tlog]
passwordlist = [spword,tpword]

curr1.execute('INSERT INTO userdata (username, password) VALUES (?,?)', (slog, spword))
curr1.execute('INSERT INTO userdata (username, password) VALUES (?,?)', (tlog, tpword))


connection1.commit()

connection2 = sqlite3.connect('scores.db')
curr2 = connection2.cursor()

# Another database has been initilaised in order to store the scores for teachers and students. 
curr2.execute('''
CREATE TABLE IF NOT EXISTS scores(
   logintype VARCHAR(255) NOT NULL,
   totalscore INTEGER(3) NOT NULL,
   timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP   
)
''')

# I have created 4 variables stored in pairs where its own columns match. 
# This is as depending on the user thats where the score is stored.
logtype1, totalscore1 = 'Teacher', 0

logtype2, totalscore2 = 'Student', 0

# This execute inserts the variables I defined into the specfic part of the table. 
# It is important to define these variables for when I want to add scores later on.
curr2.execute('INSERT INTO scores (logintype, totalscore) VALUES (?,?)', (logtype1, totalscore1))

curr2.execute('INSERT INTO scores (logintype, totalscore) VALUES (?,?)', (logtype2, totalscore2))


connection2.commit()


# The function below is used when I want to add a new value to the database
def scoreupdate(logintype, lscore):
    connection2 = sqlite3.connect('scores.db')
    curr2 = connection2.cursor()
    curr2.execute('INSERT INTO scores (logintype, totalscore) VALUES (?, ?)', (logintype, lscore))
    connection2.commit()

# The below functions are all pop up screens which will come during the game such as a piece reaching the end black or white.
# Along with when a piece is taken etc

def bendreach():
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("BLACK PIECE REACHED END", True, 'Black')
    screen.blit(text, (120, 70))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
    # Breaks when mouse is initially released so pop up doesnt go immediately
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True

    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True
                    
def wendreach():
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("WHITE PIECE REACHED END", True, 'Black')
    screen.blit(text, (120, 70))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True
    

# The two magic functions are pop ups which end the game when the magic square is reached by either the black piece or white piece.   

def magicpopupw():
    global tors
    global opposition
    global currscore
    global oppscore
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("Landed on Magic square - WIN!", True,'Black')
    screen.blit(text, (120, 70))
    text2 = font2.render(opposition+'s' + ' won game', True, 'Black')
    screen.blit(text2, (135, 130))
    if tors == 1:
       text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    else:
       text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()

    # The below code is used to avoid the error of when the page constantly closes and opens. 

    # Makes use of boolean logic and pygame functions.
 
    break_out = False 
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True

# The below pop ups follow the same logic as magicpopupw () 

def magicpopupb():
    global tors
    global opposition
    global currscore
    global oppscore
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("Landed on Magic square - WIN!", True,'Black')
    screen.blit(text, (120, 70))
    if tors == 1:
       text2 = font2.render('Teachers' + ' won game', True, 'Black')
    elif tors == 2:
       text2 = font2.render('Students' + 'won game', True, 'Black')
    screen.blit(text2, (235, 130))
    if tors == 1:
       text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    else:
       text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True


def oppwin():
    global opposition
    global currscore
    global oppscore
    global tors 
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("GAME WON!", True,'Black')
    screen.blit(text, (120, 70))
    text2 = font2.render(opposition+'s' + ' won game', True, 'Black')
    screen.blit(text2, (135, 130))
    if tors == 1:
       text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    else:
       text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True     

def torswin():
    global tors
    global opposition
    global currscore
    global oppscore
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("GAME WON!", True,'Orange')
    screen.blit(text, (120, 70))
    if tors == 1:
       text2 = font2.render('Teachers' + ' won game', True, 'Black')
    elif tors == 2:
       text2 = font2.render('Students' + 'won game', True, 'Black')
    screen.blit(text2, (235, 130))
    if tors == 1:
       text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    else:
       text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True
   

def opopup():
    global opposition
    global currscore
    global oppscore
    global tors 
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("POINT!", True,'Orange')
    screen.blit(text, (120, 70))
    text2 = font2.render(opposition+'s' + ' won point', True, 'Black')
    screen.blit(text2, (135, 130))
    if tors == 1:
       text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    else:
       text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True 

def tpopup():
    global opposition
    global currscore
    global oppscore
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("POINT!", True,'Black')
    screen.blit(text, (120, 70))
    text2 = font2.render('Teacher' + ' won point', True, 'Black')
    screen.blit(text2, (135, 130))
    text3 = font2.render('Teacher score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()

    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True

    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True

def spopup():
    global opposition
    global currscore
    global oppscore
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("POINT!", True,'Black')
    screen.blit(text, (120, 70))
    text2 = font2.render('Student' + ' won point', True, 'Black')
    screen.blit(text2, (135, 130))
    text3 = font2.render('Student score is ' + str(currscore), True, 'Black')
    screen.blit(text3, (100, 190))
    text4 = font2.render(opposition+'s' + ' score is ' + str(oppscore), True,'Black')
    screen.blit(text4, (80, 250))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
    
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True

    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True

# I have made two different textboxes one for the username to be entered and another for the password to be entered.                    
def userlogintextbox():
    global selectedbox
    text = font2.render("Username:", True , 'Black')
    screen.blit(text, (165, 180))
    button = Button(textboxtext1,(165, 200))
    button.draw()
    if button.clickcheck():
       selectedbox = 1 # This variable is used to identify which box has been clicked which allows certain code to operate. 
       
def passlogintextbox():
    global selectedbox
    text = font2.render("Password:", True, 'Black')
    screen.blit(text, (165, 280))
    button = Button(textboxtext2, (165, 300))
    button.draw()
    if button.clickcheck():
       selectedbox = 0 # Here it is made 0 to identify to my code which box is selected.
# This is where the opposition name will be entered
def oppname():
    global selectedbox
    global opposition
    text = font2.render("Opponent Name:", True, 'Black')
    screen.blit(text, (165, 380))
    button = Button(textboxtext3, (165, 400))
    button.draw()
    if button.clickcheck():
       selectedbox = 2
    opposition = textboxtext3
    
    
# This is the login function which puts all the textboxes together. 
# Inside of this function it contains the global variables selectedbox and tors.  
def login(usernamelist,passwordlist):
    global selectedbox # This variable is used to identify to the program which box has been selected and is to have actions performed to.
    global tors # This is an important variable used in many sections of my code hence i have made it global.
    # It acts as an identifier of whether a teacher or student has logged into my system.
    userlogintextbox()
    passlogintextbox()
    oppname()

    if textboxtext1 == 'Teacher':
       tors = 1
    elif textboxtext1 == 'Student':
       tors = 2

    button1 = Button('Login System', (165, 100))
    button1.draw()
       
    button2 = Button('Enter',(165, 480))
    button2.draw()
    if textboxtext1 in usernamelist and textboxtext2 == passwordlist[usernamelist.index(textboxtext1)]: 
       return button2.clickcheck()
    
    
# This is the class that is used to build all the buttons within my program and contains all the respective functions for it.
class Button:

  def __init__(self, txt, pos):
    self.text = txt
    self.pos = pos
    self.button = pygame.rect.Rect((self.pos[0], self.pos[1]), (260, 40))

  def draw(self):
    pygame.draw.rect(screen, 'dark blue', self.button, 4, 4)
    text = font1.render(self.text, True, 'Purple')
    screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))

  def draw2(self):
    pygame.draw.rect(screen, 'dark blue', self.button, 4, 4)
    text = font2.render(self.text, True, 'Red')
    screen.blit(text, (self.pos[0] + 12, self.pos[1] + 7))

  def clickcheck(self):
    global curr_mouse_state
    if self.button.collidepoint(pygame.mouse.get_pos()):
      text = font1.render(self.text, True, 'White')
      screen.blit(text, (self.pos[0] + 15, self.pos[1] + 7))
      if not curr_mouse_state:
        return False
      return True

# This class creates all of the pieces that will be used within my game
class Sprites:
      
      thickness = 15
      out = 2

      def __init__(self, row, col, colour):
          self.row = row
          self.col = col
          self.x = 0
          self.y = 0
          self.colour = colour
          self.getpos()

      def getpos(self):
          self.x = sizesq * self.col + sizesq // 2
          self.y = sizesq * self.row + sizesq // 2

      def draw(self, win):
          radius = sizesq//2 - self.thickness
          pygame.draw.circle(win, black, (self.x, self.y), radius + self.out)
          pygame.draw.circle(win, self.colour, (self.x, self.y), radius)
                     
      def wincheck(self, srow, scol, piece):
          if piece.colour == black and self.row == srow and self.col == scol:
             magicpopupb()
             return "black"
          elif piece.colour == white and self.row == srow and self.col == scol:
             magicpopupw()
             return "white"

      def piececheck(self, row, piece, board):
          if piece.colour == black and self.row == 0:
             for i, item in enumerate(board[0]):
               if repr(item) == str(black):
                 board[0][i] = 0
             bendreach()
             
          elif piece.colour == white and self.row == 7:
             for i, item in enumerate(board[7]):
                if repr(item) == str(white):
                   board[7][i] = 0
             wendreach()


      def move(self, row, col):
          self.row = row
          self.col = col
          self.getpos()

      def __repr__(self):
          return str(self.colour)

# This class is for the actual board and controls the functions that will occur within the board.                     
class Board:
     
      def __init__(self):
          self.board = []
          self.black_left = 8
          self.white_left = 8 
          self.srow = random.randrange(2,5)
          self.scol = random.randrange(0,8)
          self.create_board()

      def makesquares(self, win):
          win.fill(blue)
          for row in range(8):
              for col in range(row % 2, 8, 2):
                  type1 = row*sizesq
                  type2 = col*sizesq
                  pygame.draw.rect(win, green, (type1, type2, sizesq, sizesq)) 

      def move(self, piece, row, col):
          self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
          piece.move(row, col)

      def create_board(self):
          for row in range(rows):
            self.board.append([])
            for col in range(cols):
                if col % 2 == ((row +  1) % 2):
                    if row < 2:
                        self.board[row].append(Robber)
                    elif row > 5:
                        self.board[row].append(Police)
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
                    

        
      def draw(self, win):
          self.makesquares(win)
          overallw = None
          for row in range(rows):
              for col in range(cols):
                  piece = self.board[row][col]
                  if piece != 0:
                     piece.draw(win)
                     winner = piece.wincheck(self.srow, self.scol, piece)
                     if winner is not None:
                        overallw = winner
          return overallw
                     

      def remove(self, pieces):
          global currscore
          global oppscore
          global tors
          global datatrack
          for piece in pieces:
              self.board[piece.row][piece.col] = 0
              if piece != 0:
                 if piece.colour == black:
                    if currscore > 0:
                       currscore -= 1
                    oppscore += 1
                    opopup()
                    self.black_left -= 1
                 elif piece.colour == white :
                    if tors == 1:
                       currscore += 1
                       oppscore -= 1
                       tpopup()
                       lscore = currscore
                       scoreupdate('Teacher', lscore)
                       datatrack += 1
                       
                    elif tors == 2:
                       currscore += 1
                       oppscore -= 1
                       spopup()
                       lscore = currscore
                       scoreupdate('Student', lscore)
                       datatrack += 1
                    self.white_left -= 1
    
      def winner(self):
          if self.black_left == 0:
             oppwin()
             return 'white'
          elif self.white_left == 0:
             torswin()
             return 'black'
    
      def getallowedmoves(self, piece):
          moves = {}
          row = piece.row
          forward = piece.row + 1
          back = piece.row - 1

          if piece.colour == black:
             moves.update(self.moveforward(row -1, max(row-3, -1), -1, piece.colour, forward))
             moves.update(self.moveback(row -1, max(row-3, -1), -1 ,piece.colour, back))
          if piece.colour == white:
             moves.update(self.moveforward(row +1, min(row+3, row), 1, piece.colour, forward))
             moves.update(self.moveback(row +1, min(row+3, row),1, piece.colour, back))
          
          return moves
          
      
      def moveforward(self, start, stop, step, colour, forward, skipped = []):
            moves = {}
            last = []
            for r in range(start, stop, step):
                if forward >= rows:
                    break
                
                current = self.board[r][forward]
                if current == 0:
                    if skipped and not last:
                        break
                    elif skipped:
                        moves[(r,forward)] = last + skipped
                    else:
                        moves[(r, forward)] = last
                    
                    if last:
                        if step == -1:
                            row = max(r-3, 0)
                        else:
                            row = min(r+3, rows)
                        moves.update(self.moveback(r+step, row, step, colour, forward-2,skipped=last))
                        moves.update(self.moveforward(r+step, row, step, colour, forward+1,skipped=last))
                    break
                elif current.colour == colour:
                    break
                else:
                    last = [current]

                forward += 1
            
            return moves
      
      def moveback(self, start, stop, step, colour, back, skipped = []):
            moves = {}
            last = []
            for r in range(start, stop, step):
                if back <= 0:
                    break
                
                current = self.board[r][back]
                if current == 0:
                    if skipped and not last:
                        break
                    elif skipped:
                        moves[(r, back)] = last + skipped
                    else:
                        moves[(r, back)] = last
                    
                    if last:
                        if step == -1:
                            row = max(r+3, 0)
                        else:
                            row = min(r-3, rows)
                        moves.update(self.moveback(r+step, row, step, colour, back-1,skipped=last))
                        moves.update(self.moveforward(r+step, row, step, colour, back+2,skipped=last))
                    break
                elif current.colour == colour:
                    break
                else:
                    last = [current]

                back -= 1
            
            return moves
          



# This class controls the actual game and how it will run
class Game:
        def __init__(self, win):
            self.selected = None
            self.board = Board()
            self.turn = black
            self.allowedmoves = {}
            self.win = win
        
        def update(self):
            winner = self.board.draw(self.win)
            self.drawallowedmoves(self.allowedmoves)
            pygame.display.update()
            return winner

        def winner(self):
            return self.board.winner()

        def reset(self):
            self.selected = None
            self.board = Board()
            self.turn = black
            self.allowedmoves = {}

        def select(self, row, col):
            piece = self.board.board[row][col]
            if piece.colour == self.turn and piece != 0 :
                self.selected = piece
                self.allowedmoves = self.board.getallowedmoves(piece)
                return True
        
            if self.selected:
                result = self._move(row, col)
                if not result:
                    self.selected = None
                    self.select(row, col)
            return False

        def _move(self, row, col):
            piece = self.board.board[row][col]
            if self.selected and piece == 0 and (row, col) in self.allowedmoves:
                self.board.move(self.selected, row, col)
                skipped = self.allowedmoves[(row, col)]
                if skipped:
                    self.board.remove(skipped)
                self.change()
            else:
                return False

            return True

        def drawallowedmoves(self, moves):
            for move in moves:
                row, col = move
                pygame.draw.circle(self.win, pink, (col * sizesq + sizesq//2, row * sizesq + sizesq//2), 15)

        def change(self):
            self.allowedmoves = {}
            if self.turn == black:
               self.turn = white
            else:
               self.turn = black           



# This gets the current position of the mouse which will be useful when trying to click buttons or start games etc.
def mousepos(pos):
    
    run = True
    x, y = pos
    row = y // sizesq
    col = x // sizesq
    return row, col

# Below are more pop up functions that are used to otify the user of how much time they have keft.
# These pop ups use the same logic as the other ones above.
def onemin():
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("ONE MINUTE LEFT", True, 'Black')
    screen.blit(text, (120, 70))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True

def outoftime():
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render("OUT OF TIME!", True, 'Black')
    screen.blit(text, (120, 70))
    bbtn = Button("Okay", (125, 400))
    bbtn.draw()
    pygame.display.update()
 
    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                break_out = True


    break_out = False
    while not break_out:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if bbtn.clickcheck():
                    break_out = True

# This is the pgame loop which stands for play game.
# This function is what is called at the menu to actually run the magic square game through the loop which is contained within.
def pgame():
    run = True
    clock = pygame.time.Clock() 
    game = Game(screen)
    totaltime = 7200
    while run:
        clock.tick(fps)

        if totaltime > 0:
           totaltime = totaltime - 1

        if totaltime == 3600:
           onemin()
                               
        if totaltime == 0:
           outoftime()
           run = False

        if game.winner() != None:
           run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = mousepos(pos)
                game.select(row, col)


        winner = game.update()
        
        
        if winner == 'black':
           run = False
           
        elif winner == 'white':
           run = False

# The bottom two functions are used to retrieve all scores that have been achieved on a device.
# One is for the teachers use and the other is for the students use.
def allscoresteacher():
    curr2.execute('SELECT totalscore FROM scores WHERE logintype = \'Teacher\' ')
    result = curr2.fetchall()
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = "Here are all of the teacher scores through your games - " + str(result)
    counter = 0
    output = ""
    for char in text:
        output += char
        font_render = font2.render(output.split("\n")[-1], True, 'Black')
        if font_render.get_width() > 400:
            screen.blit(font_render, (50, 75+counter * 20))
            output = ""
            counter += 1
    font_render = font2.render(output.split("\n")[-1], True, 'Black')
    screen.blit(font_render, (50, 75+counter * 20)) 
    pygame.display.update()
    if True:
       pass

def allscoresstudent():
    curr2.execute('SELECT totalscore FROM scores WHERE logintype = \'Student\' ')
    result = curr2.fetchall()
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = "Here are all of the student scores through your games - " + str(result)
    counter = 0
    output = ""
    for char in text:
        output += char
        font_render = font2.render(output.split("\n")[-1], True, 'Black')
        if font_render.get_width() > 400:
            screen.blit(font_render, (50, 75+counter * 20))
            output = ""
            counter += 1
    font_render = font2.render(output.split("\n")[-1], True, 'Black')
    screen.blit(font_render, (50, 75+counter * 20))
    pygame.display.update()
    if True:
       pass

# The next two functions are the ones that are used to retrieve the most recent score.
# Again it is in the same pattern which involves a function for the teacher and another for the student.
def prevscoreteacher(connection2, curr2):
    curr2.execute('''SELECT * FROM scores ORDER BY timestamp DESC LIMIT 1;''')
    result = curr2.fetchone()
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])  
    font = pygame.font.Font(None, 36)
    if result:
       text = font3.render("Here is your most recent score teacher - " + str(result[1]))
    else:
       text = ("No score available", True, 'Black')
    screen.blit(text, (120, 120))
    pygame.display.update()
     
 

def prevscorestudent(connection2, curr2):
    curr2.execute('''SELECT * FROM scores ORDER BY timestamp DESC LIMIT 1;''')
    result = curr2.fetchone()
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])  
    font = pygame.font.Font(None, 36)
    if result:
       text = font3.render("Here is your most recent score student - " + str(result[1]))
    else: 
       text = ("No score available", True, 'Black')
    screen.blit(text, (120, 120))
    pygame.display.update()


# This is the scores function which is called when the user cicks teh option to view scores. 
# It contains the option to either view the latest score or all the scoresachieved.
def scores():
    global tors 
    pygame.draw.rect(screen, 'Pink', [20, 50, 480, 400])
    text = font1.render('SCORE OVERVIEWS!', True, 'Orange')
    screen.blit(text, (120, 70))
    bbtn1 =  Button('View previous score', (120, 120))
    bbtn2 = Button('View all scores', (120, 180))
    bbtn1.draw()
    bbtn2.draw()

    pygame.display.update()

    run = True
    while run:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                 run = False
              elif event.type == pygame.MOUSEBUTTONDOWN:
                   if bbtn1.clickcheck():
                      if tors == 1:
                         prevscoreteacher(connection2, curr2)

                      elif tors == 2:
                         prevscorestudent(connection2, curr2)
                                         

                   elif bbtn2.clickcheck():
                      if tors == 1:
                         allscoresteacher()
                      elif tors == 2: 
                         allscoresstudent()

# This is the main menu that contains all the options that the user is able to access.
def draw_menu():
  global main_menu
  global loginP
  main_menu = True
  loginP = False
  cnt = 0
  menu_btn = Button("Exit Magic Menu", (120, 357))
  btn1 = Button("Play", (120, 180))
  btn2 = Button("Rules", (120, 240))
  btn3 = Button("View score performance", (120, 300))
  btn4 = Button("Do not procrastinate - play for short times", (120, 120))
  menu_btn.draw()
  btn1.draw()
  btn2.draw()
  btn3.draw()
  btn4.draw2()
  if menu_btn.clickcheck():
    main_menu = False
  elif btn1.clickcheck():
    ge = True
    pgame()
  elif btn2.clickcheck():
    rulesy = True
    rules()
  elif btn3.clickcheck():
    scoring = True
    scores()


def rules():
  global cc
  global font3
  global rulesy
  global main_menu
  main_menu = False
  pygame.draw.rect(screen, 'Green', [20, 50, 480, 400])
  text = font3.render("1- Player will select a character of choice", True,'Orange')
  screen.blit(text, (120, 70))
  text2 = font3.render("2- Player will select an enemy", True, 'Orange')
  screen.blit(text2, (135, 130))
  text3 = font3.render(
      "3- Player will only be able to make one move at a time", True, 'Orange')
  screen.blit(text3, (100, 190))
  text4 = font3.render(
      "4- Pink circles will guide available positions", True,
      'Orange')
  screen.blit(text4, (80, 250))
  text5 = font2.render(
      "5- If either player lands on magic square the game will be won",
      True, 'Orange')
  screen.blit(text5, (50, 310))
  text6 = font3.render("6- There is a 2 minute time limit in the game.", True,
                       'Orange')
  screen.blit(text6, (110, 370))
  bbtn = Button("I understand", (125, 400))
  bbtn.draw()
  rulesy = not bbtn.clickcheck()

# The loop below is the starting loop for the login page which can be seen lower down with the selection statements.
run = True
while run:
      screen.fill('light blue')
      timer.tick(fps)
      if pygame.mouse.get_pressed()[0] and not prev_mouse_state:
         curr_mouse_state = True
      else:
         curr_mouse_state = False
      prev_mouse_state = pygame.mouse.get_pressed()[0]
      if loginP:
         mcnt = login(usernamelist,passwordlist)
      if main_menu:
         mcnt = draw_menu()
      elif rulesy:
         mcnt = rules()
      elif scoring:
         mcnt = scores()
      else:
         main_menu = login(usernamelist,passwordlist)   

      for event in pygame.event.get():
         if event.type == pygame.QUIT:
            run = False
         elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
               if selectedbox == 1:
                  textboxtext1 = textboxtext1[:-1]
               elif selectedbox == 0:
                  textboxtext2 = textboxtext2[:-1]
               elif selectedbox == 2:
                  textboxtext3 = textboxtext3[:-1]
            else:
               if selectedbox == 1:
                  if len(textboxtext1) < 20:
                     textboxtext1 += event.unicode
               elif selectedbox == 0:
                  if len(textboxtext2) < 20:
                     textboxtext2 += event.unicode
               elif selectedbox == 2:
                  if len(textboxtext2) < 20:
                     textboxtext3 += event.unicode

           
                    
      pygame.display.flip() 
pygame.quit()


