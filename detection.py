import cv2 as cv
import numpy as np

class Detection:

    referenceImg = None
    referenceImgWidth = 0
    referenceImgHeight = 0
    imageDetectionMethod = None


    def __init__(self, referenceImgPath, imageDetectionMethod=cv.TM_CCOEFF_NORMED):
        self.referenceImg = cv.imread(referenceImgPath, cv.IMREAD_REDUCED_COLOR_4)
            
        self.referenceImgWidth = self.referenceImg.shape[1]
        self.referenceImgHeight = self.referenceImg.shape[0]
        
        self.imageDetectionMethod = imageDetectionMethod 

    def findPosition(self, screenshotImage, threshold=0.55, debug_mode=None, windowName='Computer Vision'):
        
        result = cv.matchTemplate(screenshotImage, self.referenceImg, self.imageDetectionMethod) # Find referenceImg image on given screenshotImage

        # Filter out results using threshold
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        # Group all the locations that are in the same positions +- some pixels to create one rectangle
        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.referenceImgWidth, self.referenceImgHeight]
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

                # Draw to screenshotImage location of identified referenceImg
                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)

                    cv.rectangle(screenshotImage, top_left, bottom_right, line_color, line_type)
                elif debug_mode == 'points':
                    cv.drawMarker(screenshotImage, (center_x, center_y), marker_color, marker_type)    

        if debug_mode:
            cv.imshow(windowName, screenshotImage)
                
        
        return points