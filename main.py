import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
from windowcapture import WindowCapture
from detection import Detection
from threading import Thread

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create instance of window capture class
wincap = WindowCapture('Plants vs. Zombies')
# Create instance of detection class to find regular zombies
normalZombieDetection = Detection('regZombie.jpg')


isClickingZombie = False

# Bot actions
def clickZombie(points):
    if len(points) > 0:
        for point in points:
            target = wincap.getScreenPos(point) # Get coordinates with window offset included
            pyautogui.moveTo(x=target[0], y=target[1])
            pyautogui.click()
            pyautogui.click()
            pyautogui.click()

    global isClickingZombie
    isClickingZombie = False

# FPS timer
loop_time = time()

while (True):
    
    screenshot = wincap.takeScreenshot() # Take screenshot

    normalZombiePoints = normalZombieDetection.findPosition(screenshot, threshold=0.50, debug_mode='rectangles') # Get the zombie locations


    if not isClickingZombie:
        isClickingZombie = True
        t = Thread(target=clickZombie, args=(normalZombiePoints,)) # Create new thread to click on zombies
        t.start()

 
    print('FPS {}'.format(1 / (time() - loop_time))) # Display FPS
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Program Exited')  