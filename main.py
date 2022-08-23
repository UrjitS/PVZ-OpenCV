# ep1 https://www.youtube.com/watch?v=ffRYijPR8pk&ab_channel=LearnCodeByGaming
# import cv2 as cv
# import numpy as np

# haystack_img = cv.imread('heystack.jpg', cv.IMREAD_REDUCED_COLOR_4)
# needle_img = cv.imread('regZombie.jpg', cv.IMREAD_REDUCED_COLOR_4)

# result = cv.matchTemplate(haystack_img, needle_img, cv.TM_CCOEFF_NORMED)

# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
# cv.imshow('Result1', result)
# threshold = 0.8
# if max_val >= threshold:
#     print('found needle')

#     needle_w = needle_img.shape[1]
#     needle_h = needle_img.shape[0]

#     top_left = max_loc
#     bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)

#     cv.rectangle(haystack_img, top_left, bottom_right, color=(0,255,0), thickness=2, lineType=cv.LINE_4)

#     cv.imshow('Result', haystack_img)
#     cv.waitKey()
# else:
#     print('Not found needle')

# Ep 2 
# import cv2 as cv
# import numpy as np


# def findClickPosition(needle_img_path, haystack_img_path, threshold=0.55, debug_mode=None, windowName='Matches'):

#     haystack_img = cv.imread(haystack_img_path, cv.IMREAD_REDUCED_COLOR_4)
#     needle_img = cv.imread(needle_img_path, cv.IMREAD_REDUCED_COLOR_4)

#     needle_w = needle_img.shape[1]
#     needle_h = needle_img.shape[0]

#     method = cv.TM_CCOEFF_NORMED

#     result = cv.matchTemplate(haystack_img, needle_img, method)


#     locations = np.where(result >= threshold)
#     locations = list(zip(*locations[::-1]))


#     rectangles = []

#     for loc in locations:
#         rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
#         rectangles.append(rect)
        

#     rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) 

#     points = []

#     if len(rectangles):
#         print('found needle')


#         line_color = (0,255,0)
#         line_type =  cv.LINE_4
#         marker_color = (0, 0, 255)
#         marker_type = cv.MARKER_CROSS

#         for (x, y, w, h) in rectangles:

#             # Determine Center Positions
#             center_x = x + int(w/2)
#             center_y = y + int(h/2)

#             # Save points
#             points.append((center_x, center_y))

#             if debug_mode == 'rectangles':
#                 top_left = (x, y)
#                 bottom_right = (x + w, y + h)

#                 cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
#             elif debug_mode == 'points':
#                 cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)    

#         if debug_mode:
#             cv.imshow(windowName, haystack_img)
#             cv.waitKey()
    
#     return points

# regZombiePoints = findClickPosition('regZombie.jpg', 'heystack2.jpg', threshold=0.45, debug_mode='rectangles')
# coneZombiePoints = findClickPosition('coneZombie.jpg', 'haystack3.jpg', threshold=0.55, debug_mode='rectangles', windowName='Cone')
# coneZombiePoints = findClickPosition('metalZombie.jpg', 'haystack3.jpg', threshold=0.55, debug_mode='rectangles', windowName='Metal')

# print(regZombiePoints)
# print(coneZombiePoints)

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
objDetection = Detection('regZombie.jpg')

isClickingZombie = False

def clickZombie(points):
    if len(points) > 0:
            targets = points
            target = wincap.getScreenPos(targets[0])
            pyautogui.moveTo(x=target[0], y=target[1])
            pyautogui.click()

    global isClickingZombie
    isClickingZombie = False

loop_time = time()

while (True):
    
    screenshot = wincap.takeScreenshot()

    
    points = objDetection.findPosition(screenshot, threshold=0.45, debug_mode='rectangles')

    if not isClickingZombie:
        isClickingZombie = True
        t = Thread(target=clickZombie, args=(points,))
        t.start()

    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done')  