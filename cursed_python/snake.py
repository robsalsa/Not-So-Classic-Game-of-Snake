import pyautogui
import keyboard
import time

width=20
hight=9

app_distance_x = 95
app_distance_y = 105

app_starting_line_x = 50
app_starting_line_y = 30

current_x= app_starting_line_x
current_y= app_starting_line_y

grid = []

snake_body=[(0,0)]
direction="Stop"
running=True



def set_grid():
    cols = 19
    rows = 9
    global grid
    grid=[]
    for innie in range (rows):
        row_center=[]
        for outtie in range (cols):
            center_x =  app_starting_line_x + (outtie * app_distance_x)
            center_y =  app_starting_line_y + (innie * app_distance_y)
            row_center.append((center_x, center_y))
        grid.append(row_center)

def snake_location():
    x,y=grid[0][0]
    pyautogui.moveTo(x,y)

def button_comp(event):
    global direction, running
    if event.name == 'w' and direction != "down":
        direction = "up"
    elif event.name == 's' and direction != "up":
        direction = "down"
    elif event.name == 'a' and direction != "right":
        direction = "left"
    elif event.name == 'd' and direction != "left":
        direction = "right"
    elif event.name == 'p':
        running = False

keyboard.on_press(button_comp)

def get_next(pos):
    row,col = pos
    if direction == "up":
        return (row-1, col)
    elif direction == "down":
        return (row+1, col)
    elif direction == "left":
        return (row, col-1)
    elif direction == "right":
        return (row, col+1)
    return pos

def perform_step():
    global snake_body

    head = snake_body[0]
    next_pos = get_next(head)

    if not (0 <= next_pos[0] < len(grid) and 0 <= next_pos[1] < len(grid[0])):
        return

    x,y=grid[next_pos[0]][next_pos[1]]
    pyautogui.moveTo(x,y)
    snake_body[0]=next_pos
    
    # # NORMAL MOVE (no apple)
    # if next_pos not in initial_apples:
    #     x,y = grid[next_pos[0]][next_pos[1]]
    #     pyautogui.moveTo(x,y)
    #     snake_body[0] = next_pos
    #     return


set_grid()
snake_location()
pyautogui.moveTo(*grid[0][0])

while running:
    perform_step()
    # time.sleep(0.1)