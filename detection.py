import cv2 as cv
import numpy as np

class Detection:

    needle_img = None
    needle_w = 0
    needle_h = 0
    method = None


    def __init__(self, needle_img_path, method=cv.TM_CCOEFF_NORMED):
        self.needle_img = cv.imread(needle_img_path, cv.IMREAD_REDUCED_COLOR_4)
            
        self.needle_w = self.needle_img.shape[1]
        self.needle_h = self.needle_img.shape[0]
        
        self.method = method 

    def findPosition(self, haystack_img, threshold=0.55, debug_mode=None, windowName='Computer Vision'):
        
        result = cv.matchTemplate(haystack_img, self.needle_img, self.method)


        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))


        rectangles = []

        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.needle_w, self.needle_h]
            rectangles.append(rect)
            

        rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5) 

        points = []

        if len(rectangles):


            line_color = (0,255,0)
            line_type =  cv.LINE_4
            marker_color = (0, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:

                # Determine Center Positions
                center_x = x + int(w/2)
                center_y = y + int(h/2)

                # Save points
                points.append((center_x, center_y))

                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)

                    cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
                elif debug_mode == 'points':
                    cv.drawMarker(haystack_img, (center_x, center_y), marker_color, marker_type)    

        if debug_mode:
            cv.imshow(windowName, haystack_img)
                
        
        return points

# regZombiePoints = findClickPosition('regZombie.jpg', 'heystack2.jpg', threshold=0.45, debug_mode='rectangles')
# coneZombiePoints = findClickPosition('coneZombie.jpg', 'haystack3.jpg', threshold=0.55, debug_mode='rectangles', windowName='Cone')
# coneZombiePoints = findClickPosition('metalZombie.jpg', 'haystack3.jpg', threshold=0.55, debug_mode='rectangles', windowName='Metal')

# print(regZombiePoints)
# print(coneZombiePoints)