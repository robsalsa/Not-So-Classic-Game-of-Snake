import pyautogui

print("\n running a test \n")

app_distance_x = 85
app_distance_y = 105
app_starting_line_x = 50
app_starting_line_y = 30

app_count_x = 0
app_count_y = 0

app_movement_speed = .2



#pyautogui.moveTo(50,30) ##This is the dead center of the First App
# pyautogui.moveTo(50,135) ## This is the dead center of the Second Row First App
# pyautogui.moveTo(135,30) ## 
# pyautogui.moveTo(135,135)

# # this should point at the first app
pyautogui.moveTo(app_starting_line_x + (app_distance_x * app_count_x), app_starting_line_y + (app_distance_y * app_count_y)) 

# Look at all apps in the X axis 
# 10 to the app count == half of the screen 
# 21 to the app count == full screen

# Look at all apps in the Y axis 
# 4 to the app count == half of the screen
# 8 to the app count == full screen

total_moves = 20
pyautogui.mouseDown(button='left')
for innie in range(total_moves):
    app_count_x += 1
    # app_count_y += 1
    pyautogui.moveTo(app_starting_line_x + (app_distance_x * app_count_x), app_starting_line_y + (app_distance_y * app_count_y), duration=app_movement_speed) 
pyautogui.mouseUp(button='left')

# Combining both X and Y axis
# total_x = 10
# pyautogui.mouseDown(button='left')
# for innie in range(total_x):
#     app_count_x += 1
#     # Keep Y progressing with X so movement passes through the middle around x=10, y=4.
#     app_count_y = round((8 / 20) * app_count_x)
    
#     pyautogui.moveTo(
#         app_starting_line_x + (app_distance_x * app_count_x),
#         app_starting_line_y + (app_distance_y * app_count_y),
#         duration=app_movement_speed,
#         # tween=pyautogui.easeInOutQuad,
#     ) 
# pyautogui.mouseUp(button='left')




# pyautogui.click()
