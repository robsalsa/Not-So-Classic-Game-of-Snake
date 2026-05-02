import pyautogui

# pyautogui.moveTo(46,30) #dead-on
#pyautogui.moveTo(46, 135) #dead-on row-2, col-1
pyautogui.moveTo(140, 30)

# for innie in range (9):
#     y = 30+(105*innie)
 #   pyautogui.moveTo(46,y,duration=0.8)

for outtie in range (19):
    x=46+(95*outtie)
    pyautogui.moveTo(x,30)







# x,y = pyautogui.position()
# print(x,y)