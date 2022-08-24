import cv2 as cv
import numpy as np
import os
import pyautogui
from time import time
from windowcapture import WindowCapture
from detection import Detection
from threading import Thread

os.chdir(os.path.dirname(os.path.abspath(__file__)))


wincap = WindowCapture('Plants vs. Zombies')

normalZombieDetection = Detection('regZombie.jpg')


isClickingZombie = False

def clickZombie(points):

    if len(points) > 0:
        for point in points:
            target = wincap.getScreenPos(point)
            pyautogui.moveTo(x=target[0], y=target[1])
            pyautogui.click()
            pyautogui.click()
            pyautogui.click()
            pyautogui.click()
            

    global isClickingZombie
    isClickingZombie = False

loop_time = time()

while (True):
    
    screenshot = wincap.takeScreenshot()

    normalZombiePoints = normalZombieDetection.findPosition(screenshot, threshold=0.50, debug_mode='rectangles')


    if not isClickingZombie:
        isClickingZombie = True
        t = Thread(target=clickZombie, args=(normalZombiePoints,))
        t.start()


    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')  