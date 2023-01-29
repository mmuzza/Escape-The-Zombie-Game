######################################################
# Project: Midterm Project
# UIN: 661657007
# repl.it URL: https://replit.com/@CS111-Fall2021/Project-2-MuhammadMuzzam5#main.py
######################################################

import turtle
import random
import time

#board functions
def refresh_game_screen(over):
  t = actors["pen"]["t"]
  t.clear()
  t.color('white')
  style = ('Courier', 8)
  t.penup()
  if over:
    t.goto(12, -65)
  else:
    t.goto(164, 63.0)
  t.write('Lives ' + str(game['lives']), font=style, align='center', move=True)
  if over:
    t.goto(12, -90)
  else:
    t.goto(164.0, 24.0)
  t.write('Score '+str(game['score']), font=style, align='center', move=True)
  if over:
    t.goto(12, -116)
  else:
    t.goto(164.0, -15)
  t.write('Level ' + str(game['level']), font=style, align='center', move=True)
  t.pendown()
  t.hideturtle()
  screen.update()

def set_game_over_screen():
  time.sleep(0.25)
  screen.clear()
  screen.bgpic("assets/screen/game_over.gif")
  refresh_game_screen(True)

#drawing turtle functions
def draw_object(t, x, y):
  t.clear()
  t.penup()
  t.speed('fastest')
  t.goto(x,y)
  t.showturtle()
  t.pendown()

def draw_player():
  x = actors["player"]["x"]
  y = actors["player"]["y"]
  t = actors["player"]["t"]
  if game['direction'] == 'up':
      actors["player"]["t"].shape((playerUpGif+"_"+str(game["step"])).replace(".gif", "" ) + ".gif")
  elif game['direction'] == 'down':
    actors["player"]["t"].shape((playerDownGif+"_"+str(game["step"])).replace(".gif", "" ) + ".gif")
  elif game['direction'] == 'right':
    actors["player"]["t"].shape((playerRightGif+"_"+str(game["step"])).replace(".gif", "" ) + ".gif")
  elif game['direction'] == 'left':
    actors["player"]["t"].shape((playerLeftGif+"_"+str(game["step"])).replace(".gif", "" ) + ".gif")
  draw_object(t, x, y)
 
def draw_dumbell():
  x = actors["dumbell"]["x"]
  y = actors["dumbell"]["y"]
  t = actors["dumbell"]["t"]
  draw_object(t, x, y)

def draw_zombie(row, col):
  x = actors["zombie"][row][col]["x"]
  y = actors["zombie"][row][col]["y"]
  t = actors["zombie"][row][col]["t"]
  if x <= xMax and x >= xMin:
    draw_object(t, x, y)
  
  
#actor movement functions
def initialize_actors():
  actors["player"]["x"] = 0
  actors["player"]["y"] = yMin
  actors["dumbell"]["x"] = random.choice(range(xMin, xMax, actorSize))
  actors["dumbell"]["y"] = yMax
  draw_player()
  draw_dumbell()
  y = yMax - actorSize
  for row, obj in enumerate(actors["zombie"]):
    for col, h in enumerate(obj):
      h["speed"] = 0.008 * (row+1)
      h["y"] = y
      h["x"] = random.choice(range(xMin, xMax, actorSize))
      draw_zombie(row, col)
    y = y - actorSize  
    
def hide_actors():
  actors["player"]["t"].hideturtle()
  actors["dumbell"]["t"].hideturtle()
  for row, obj in enumerate(actors["zombie"]):
    for h in obj:
      if row %2 == 0:
        h["t"].shape(zombieLeftGif)
      else:
        h["t"].shape(zombieRightGif)
      h["t"].hideturtle()


def init_board():
    screen.bgpic(boardGif)
    game["stop"] = False
    game['direction'] = 'down'
    # hide turtles and draw image
    actors["player"]['t'].shape(playerDownGif)
    actors["dumbell"]['t'].shape(dumbellGif)
    hide_actors()
    screen.update()

def register_player_events():
    # register events
    screen.onkey(move_player_up, "Up")
    screen.onkey(move_player_down, "Down")
    screen.onkey(move_player_right, "Right")
    screen.onkey(move_player_left, "Left")

def unregister_player_events():
    # register events
    screen.onkey(None, "Up")
    screen.onkey(None, "Down")
    screen.onkey(None, "Right")
    screen.onkey(None, "Left")

def start_game():
  init_board()
  initialize_actors()
  refresh_game_screen(False)
  register_player_events()
  z = 1
  i = 1
  b = 1
  while game['stop'] == False:
    collision = False

    screen.bgpic((boardGif+"_"+str(b)).replace(".gif", "" ) + ".gif")

    for row, obj in enumerate(actors["zombie"]):
      for col, h in enumerate(obj):
        pos = h["x"] + (h["speed"] * game['level'])
        if row % 2 == 0:
          pos = h["x"] - (h["speed"] * game['level'])
          h["t"].shape((zombieLeftGif+"_"+str(z)).replace(".gif", "" ) + ".gif")
        else:
          h["t"].shape((zombieRightGif+"_"+str(z)).replace(".gif", "" ) + ".gif")
        if pos > xMax:
          if pos > xMax + 30:
            pos = xMin
          h["t"].hideturtle()
        elif pos < xMin:
          if pos < xMin - 30:
            pos = xMax
          h["t"].hideturtle()
        h["x"] = pos
        draw_zombie(row, col)
        collision = check_collision(h["x"], h["y"], True)
        if collision:
          break
      if collision:
        break
    i = i + 1
    if i % 15 == 0:
      z = z+1
      if z > 8:
        z = 1

    if i % 60 == 0:
      b = b+1
      if b > 3:
        b = 1
    screen.update()

def move_player_left():
  if game['stop'] == False:
    actors["player"]['t'].shape(playerLeftGif)
    xpos = actors["player"]["x"] - 10
    if xpos >= xMin:
      move_player(xpos, actors["player"]["y"], "left")
    
def move_player_right():
  if game['stop'] == False:
    actors["player"]['t'].shape(playerRightGif)
    xpos = actors["player"]["x"] + 10
    if xpos <= xMax:
      move_player(xpos, actors["player"]["y"], "right")

def move_player_down():
  if game['stop'] == False:
    actors["player"]['t'].shape(playerDownGif)
    ypos = actors["player"]["y"] - 30
    if ypos >= yMin:
      move_player(actors["player"]["x"], ypos, "down")

def move_player_up():
  if game['stop'] == False:
    actors["player"]['t'].shape(playerUpGif)
    ypos = actors["player"]["y"] + 30
    if ypos <= yMax:
      move_player(actors["player"]["x"], ypos, "up")
  
def move_player(xpos, ypos, dir):
  if dir == game["direction"]:
    game["step"] = game["step"] + 1
    if game["step"] > 4:
      game["step"] = 1
  else:
    game["direction"] = dir
    game["step"] = 1
  actors["player"]["x"] = xpos
  actors["player"]["y"] = ypos
  draw_player()
  screen.update()
  collided = check_collision(actors["dumbell"]["x"],actors["dumbell"]["y"], False)
  if collided == False:
    for obj in actors["zombie"]:
      for h in obj:
        collided = check_collision(h["x"],h["y"], True)
        if collided:
          break
  
def check_collision(x, y, iszombie):
  actorPosx = actors["player"]["x"]
  actorPosy = actors["player"]["y"]
  yCollision = actorPosy == y
  xNoCollision = actorPosx + 15 <= x or actorPosx >= x + 15

  if yCollision and xNoCollision == False:
    unregister_player_events()
    game['stop'] = True
    if iszombie:  
      game["lives"] = game["lives"] - 1
      if game["lives"] < 0:
        game["lives"] = 0
      if game["lives"] == 0:
        set_game_over_screen()
      else:
        start_game()
    else:
      game['score'] = game['score'] + game['level']
      game['level'] = game['level'] + 1
      start_game()
    return True
  return False
       


if __name__ == "__main__":

    #declare global variables
    actors = {
      "pen":{"t":turtle.Turtle(visible=False)},
      "player": {"x":-120, "y":0, "t":turtle.Turtle(visible=False)},
      "dumbell": {"x":0, "y":0, "t":turtle.Turtle(visible=False)},
      "zombie": [
        [{"x":0, "y":0, "t": turtle.Turtle(visible=False),"speed":0} for x in range(2)]
        for x in range(8)]
    }
    game = {
      "level": 1,
      "score": 0,
      "lives": 3,
      'stop': False,
      'direction':'down',
      'step': 1
    }
    stopGameRound = False

    #create screensize variables
    height = 300
    width = 400
    scoreWidth = 100
    actorSize = 30
    xMin = int(-width/2) + 15
    xMax = int(width/2) - scoreWidth - 15
    yMin = int(-height/2) + 15
    yMax = int(height/2) - 15

    #create empty screen
    screen = turtle.Screen()
    screen.screensize(width, height)
    screen.bgpic('assets/screen/start.gif')
    screen.title("Dead Workout")
     
    #register shapes and associate them to actors/turtles
    playerDownGif = 'assets/actors/player_down.gif'
    playerUpGif = 'assets/actors/player_up.gif'
    playerRightGif = 'assets/actors/player_right.gif'
    playerLeftGif = 'assets/actors/player_left.gif'
    zombieRightGif = 'assets/actors/zombie_right.gif'
    zombieLeftGif = 'assets/actors/zombie_left.gif'
    dumbellGif = 'assets/actors/dumbell.gif'
    boardGif = 'assets/screen/board.gif'
    failGif = 'assets/screen/fail.gif'
    passGif = 'assets/screen/pass.gif'

    screen.addshape(playerDownGif)
    screen.addshape(playerUpGif)
    screen.addshape(playerRightGif)
    screen.addshape(playerLeftGif)
    screen.addshape(zombieRightGif)
    screen.addshape(zombieLeftGif)
    screen.addshape(dumbellGif)
    screen.addshape(passGif)
    screen.addshape(failGif)
    
    for i in range(1,9):
      screen.addshape((zombieLeftGif+"_"+str(i)).replace(".gif", "" ) + ".gif")
      screen.addshape((zombieRightGif+"_"+str(i)).replace(".gif", "" ) + ".gif")    

    for i in range(1,5):
      screen.addshape((playerUpGif+"_"+str(i)).replace(".gif", "" ) + ".gif") 
      screen.addshape((playerDownGif+"_"+str(i)).replace(".gif", "" ) + ".gif") 
      screen.addshape((playerRightGif+"_"+str(i)).replace(".gif", "" ) + ".gif") 
      screen.addshape((playerLeftGif+"_"+str(i)).replace(".gif", "" ) + ".gif") 
    
    screen.tracer(0,0)

    # #register turtle events
    screen.onkey(start_game, "Return")    
    screen.listen()
    turtle.mainloop()