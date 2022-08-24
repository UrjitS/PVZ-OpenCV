import win32gui, win32ui, win32con
import numpy as np

class WindowCapture:

    width = 0 
    height = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    hwnd = None

    def __init__(self, window_name=None):
        # Find and capture window or entire screen
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))

        # Adjust width and height to the screens
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]

        # Crop titlebar & border
        border_pixels = 8
        titlebar_pixels = 60
        self.width = self.width - (border_pixels * 2)
        self.height = self.height - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y

    # Modified code of https://stackoverflow.com/questions/3586046/fastest-way-to-take-a-screenshot-with-python-on-windows
    def takeScreenshot(self):
        # Get window from os and convert to image for opencv
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()

        dataBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.width, self.height) , dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        signedIntArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        img = np.ascontiguousarray(img)

        return img

    def getScreenPos(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y) # include calculated offset to given positions