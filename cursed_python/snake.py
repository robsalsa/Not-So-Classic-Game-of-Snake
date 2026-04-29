import pyautogui
import keyboard

# from PIL import ImageGrab
import random
import time 
#the grid is 20-long x 9-high = 180 spots to move to.

width=20
hight=9

app_distance_x = 85     #my math is off FIX IT IDIOT
app_distance_y = 105


app_starting_line_x = 50
app_starting_line_y = 30


current_x= app_starting_line_x
current_y= app_starting_line_y

grid = []


snake_head=(0,0)
direction="Stop"
running=True

print("\n WARNING: This program will steal your mouse for a bit")
print("It is recomended that you do not press anything other than the designated buttons")
print("... or dont i dont really care tbh\n")





# Set Up the game: Creating a Grid to play and easy finding of items
def set_grid():
    cols = 21 #actual is 19 but for full play is 20 and buffer is 21
    rows = 10 #actual is 8 but full play is 9 and buffer is 10  
    global grid
    
    for innie in range (rows):
        row_center=[]
        for outtie in range (cols):
            center_x =  app_starting_line_x + (outtie * app_distance_x)
            center_y =  app_starting_line_y + (innie * app_distance_y)
            row_center.append((center_x, center_y))
        grid.append(row_center)
    return grid
    
    
def snake_location():
    global snake_head
    snake_head = (0,0)
    x,y=grid[0][0]
    pyautogui.moveTo(x,y)
    
    
    
def go_down():
    global direction
    if direction != "up":
        direction = "down"
def go_up():
    global direction     
    if direction != "down":
        direction = "up"
def go_right():
    global direction         
    if direction !="left":
        direction = "right"
def go_left():
    global direction  
    if direction != "right":
        direction = "left"
        
        
def move():
    global snake_head, direction
    row,col=snake_head
    
    if direction == "up":
        row -= 1
    elif direction == "down":
        row+=1
    elif direction =="right":
        col+=1
    elif direction == "left":
        col-=1
        
    if 0<=row < len(grid) and 0<=col <len(grid[0]):
        snake_head=(row,col)
        
        x,y = grid[row][col]
        pyautogui.moveTo(x,y)
        
def button_comp(event):
    global direction, running
    if event.name == 'w':
        direction = "up"
    elif event.name == 's':
        direction = "down"
    elif event.name == 'a':
        direction = "left"
    elif event.name == 'd':
        direction = "right"
    elif event.name == 'p':
        running = False
        print("GAME KILLED!")
    
    
keyboard.on_press(button_comp)        
set_grid()
snake_location()
print("controls are wasd")

while running:
    move()
    time.sleep(0.3)



 