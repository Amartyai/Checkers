from processing import *

#Defining colors
RED = "#FF2200"
BLACK = "#0F0F0F"
GOLD = "#FFCC00"
SILVER = "#CCCCCC"
GREEN = "#00CC77"
BLUE = "#0066FF"
arr = []


  
#Creating board (stored in array)
for i in range(8):
    arr.append([])
    for j in range(8):
      arr[i].append(None)
      
x_value = 0
y_value = 0
count = 0
#Kills piece when called 
def kill(xcoord,ycoord):
  arr[int(xcoord)][int(ycoord)] = None
    
#piece class
############################################Piece############################################
class Piece:
  def __init__(self,color):
    self.color=color
    self.isKing = False
    
  #Piece stores its own color  
  def getColor(self):
    return self.color
    


#Board Class
###########################################Board###############################################
class Board:
  def __init__(self):
    #Starting Positions
    redini = [[0,1],[0,3],[0,5],[0,7],[1,0],[1,2],[1,4],[1,6],[2,1],[2,3],[2,5],[2,7]]
    blackini = [[5,0],[5,2],[5,4],[5,6],[6,1],[6,3],[6,5],[6,7],[7,0],[7,2],[7,4],[7,6]]
    #Setting Starting Positions
    for i in range(len(redini)):
        arr[redini[i][0]][redini[i][1]] = Piece(RED)
    for i in range(len(blackini)):
        arr[blackini[i][0]][blackini[i][1]] = Piece(BLACK)
  
##########################################GameEngine##########################################

class GameEngine:
  def __init__ (self):
    self.b = Board()
    self.redTurn = True
    self.first_click = (-10,-10)
  
  #DISPLAY
  #Draws board and pieces
  def display (self):
    global pic1, pic2
    for j in range(0,8):
      for i in range(0,8):
        if j%2 == 0:
          if i%2 == 0:
            fill(128,128,255)
          elif i%2 != 0:
            fill(64,192,255)
        else:
          if i%2 == 0:
            fill(64,192,255)
          elif i%2 != 0:
            fill(128,128,255)
        noStroke()
        rect(i*50,j*50,50,50)
    #draws selection indicator and makes pieces king if necessary
    for i in range(len(arr)):
        for j in range(len(arr)):
          fill(GOLD)
          if arr[i][j] != None and arr[i][j].isKing == False:
              fill(arr[i][j].getColor())
              ellipse(i*50+25,j*50+25,40,40)
          elif arr[i][j] != None and arr[i][j].isKing == True and arr[i][j].getColor() == RED:
            image(pic1,i*50,j*50)
          elif arr[i][j] != None and arr[i][j].isKing == True and arr[i][j].getColor() == BLACK:
            image(pic2,i*50,j*50)
    
  #Can get x,y coordinates of any board coordinate
  def getCoords (self,col, row):
    xcoord = (50*col)
    ycoord = (50*row)
    return xcoord, ycoord
   
  def move(self,x1,y1,x2,y2):
    #Moves piece
    arr[x2][y2]=arr[x1][y1]
    kill(x1,y1)
    #set isKing() property
    if x2 == 7 and arr[x2][y2].getColor() == RED:
      arr[x2][y2].isKing = True
        
    if x2 == 0 and arr[x2][y2].getColor() == BLACK:
      arr[x2][y2].isKing = True

    
  #Figures out whether a move is legal or not
  def legal_moves(self,x1,y1,x2,y2):
    x_inc = 0
    y_inc = 0

    if x2 < x1 and arr[x1][y1].getColor() == RED and arr[x1][y1].isKing == False:
      return False
    elif x2 > x1 and arr[x1][y1].getColor() == BLACK and arr[x1][y1].isKing == False:
      return False
    elif abs(x2-x1) != abs(y2-y1) or x2-x1 == 0:
      return False
    elif abs(x2-x1) != 1:
      #Set the increments in the direction of the move
      if y2 - y1 > 0:
        y_inc = 1
      else:
        y_inc = -1
      if x2 - x1 > 0:
        x_inc = 1
      else:
        x_inc = -1
        
      for i in range(1,abs(x2-x1),2):
        if arr[x1+(i*x_inc)][y1+(i*y_inc)] == None or arr[x1+(i+1)*x_inc][y1+(i+1)*y_inc] != None or arr[x1+(i*x_inc)][y1+(i*y_inc)].getColor() == self.now_color:
          return False
    return True
    
  
  #Flips color after turn
  def flipColor(self):
    if self.redTurn:
      self.redTurn = False
    else:
      self.redTurn = True
  #Returns current color turn
  def now_color(self):
    if self.redTurn:
      return RED
    else:
      return BLACK
  
  def select_square(self):
    global count, x_value, y_value, pic1, pic2
    x_inc = 0
    y_inc = 0
    g.display()
    #Count represents which clik a color is on
    if count == 1:
      if arr[x_value][y_value] != None:
        if arr[x_value][y_value].getColor() == self.now_color() and arr[x_value][y_value].isKing==False:
          fill(255)
          #Selection indicator
          rect(x_value*50,y_value*50,50,50)
          fill(arr[x_value][y_value].getColor())
          ellipse((x_value*50)+25,(y_value*50)+25,40,40)
          self.first_click = (x_value,y_value)
        elif arr[x_value][y_value].getColor() == self.now_color() and arr[x_value][y_value].isKing==True:
          fill(255)
          #Image if king
          rect(x_value*50,y_value*50,50,50)
          if arr[x_value][y_value].getColor() == RED:
            image(pic1,x_value*50,y_value*50)
          else:
            image(pic2,x_value*50,y_value*50)
          self.first_click = (x_value,y_value)
        else:
          #If certain color's turn and they are mving opposite colors piece, clicks = 0
          count = 0
      else:
        #If empty,
          count = 0
    elif count == 2:
      #If two clicks,
      if arr[x_value][y_value] == None:
        x1, y1 = self.first_click
        if x1 == x_value and y1 == y_value:
          count = 0
          first_selected = (0,0)
        #Check if legal move,
        elif self.legal_moves(x1,y1,x_value,y_value):
          #If so then move piece
          self.move(x1,y1,x_value,y_value)
          if y_value - y1 > 0:
            y_inc = 1
          else:
            y_inc = -1
          if x_value - x1 > 0:
            x_inc = 1
          else:
            x_inc = -1
          #Kill piece if jumped over
          for i in range(1,abs(x_value-x1)):
            if arr[x1+(x_inc*i)][y1+(y_inc*i)] != None:
              kill(x1+(x_inc*i),y1+(y_inc*i))
          #Clicks is 0
          #next colors turn
          count = 0
          self.flipColor()
          
        else:
          #If second click is not legal, make them choose new second click
          count = 1
     
      else:
        #if first click is not legal, make them choose again
        count = 0
    b = 0
    c = 0
    #If a color has won, makes large text saying (blank) has won
    for i in range(0,len(arr)):
      for j in range(0,len(arr)):
        if arr[i][j] != None and arr[i][j].getColor() == RED:
          b += 1
        elif arr[i][j] != None and arr[i][j].getColor() == BLACK:
          c += 1
    if b == 0:
      textSize(40)
      text("Black Wins!!!",75,215)
    elif c == 0:
      textSize(40)
      text("Red Wins!!!",100,215)
g = GameEngine()


  
def setup ():
  global pic1,pic2
  size(400,400)
  pic1 = loadImage("crown_red_50.png")
  pic2 = loadImage("crown_black_50.png")
  print("Red Starts")
  g = GameEngine()
  g.display()
  b = Board()

#If mouse clicked call select square
def mouseClicked ():
  global count, x_value, y_value
  count += 1
  x_value = mouseX//50
  y_value = mouseY//50
  g.select_square()
run()
