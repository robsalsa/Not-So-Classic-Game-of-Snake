import pyautogui

import random
import time 
#the grid is 20-long x 9-high = 180 spots to move to.

width=20
hight=9

extra_space_on_col=21 # 1 by 1 buffer

app_distance_x = 85
app_distance_y = 105


app_starting_line_x = 50
app_starting_line_y = 30


current_x= app_starting_line_x
current_y= app_starting_line_y


print("\n WARNING: This program will steal your mouse for a bit")
print("It is recomended that you do not press anything other than the designated buttons")
print("... or dont i dont really care tbh\n")





# Set Up the game: Creating a Grid
# cols = 20 #this is the y
# rows = 8 #this is the x
# grid = []

# for innie in range (rows):
#     row_center=[]
#     for outtie in range(cols):
#         center_x= app_starting_line_x + (outtie * app_distance_x)
#         center_y = app_starting_line_y + (innie * app_distance_y)
        
#         row_center.append((center_x, center_y))
#     grid.append(row_center)
    


# pyautogui.moveTo(grid[0][0])
# pyautogui.moveTo(grid[4][10])

def move_test():
    global current_x, current_y
    
    pyautogui.mouseDown()
    time.sleep(0.1)
    
    for innie in range(10):
        current_x=innie
        pyautogui.moveTo(app_starting_line_x+(app_distance_x * current_x), app_starting_line_y + (app_distance_y * current_y))
        
        
    for outtie in range(9):    
        current_y=outtie
        pyautogui.moveTo(app_starting_line_x+(app_distance_x * current_x), app_starting_line_y + (app_distance_y * current_y))
        time.sleep(0.1)
    pyautogui.mouseUp()
    
def go_back():
    global current_x, current_y
    pyautogui.mouseDown()
    time.sleep(0.1)
    
    for innie in range(current_x, -1, -1):
        current_x=innie
        pyautogui.moveTo(app_starting_line_x+(app_distance_x * current_x), app_starting_line_y + (app_distance_y * current_y))
        
    for outtie in range(current_y, -1, -1):    
        current_y=outtie
        pyautogui.moveTo(app_starting_line_x+(app_distance_x * current_x), app_starting_line_y + (app_distance_y * current_y))
        time.sleep(0.1)
    pyautogui.mouseUp()
    

        
        
pyautogui.moveTo(app_starting_line_x, app_starting_line_y)
move_test()
go_back()
     
