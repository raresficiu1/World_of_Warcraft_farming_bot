import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4
import time
from PIL import Image
from getshortestline import getClosestPoint,getDistancetoPoint
from nextStep import next
from pynput.mouse import Listener
import math

calibrationScreen=False
calibrationDirection=False
direction=[0,0]

def grab_screen(region=None):
    hwin = win32gui.GetDesktopWindow()

    if region:
        left, top, x2, y2 = region
        width = x2 - left + 1
        height = y2 - top + 1
    else:
        width = win32api.GetSystemMetricwqs(win32con.SM_CXVIRTUALSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

    hwindc = win32gui.GetWindowDC(hwin)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

    signedIntsArray = bmp.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype='uint8')
    img2 = np.fromstring(signedIntsArray, dtype='uint8')

    img.shape = (height, width, 4)
    img2.shape = (height, width, 4)

    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img, img2

def update_direction(points):
    global direction
    direction_aux=[0,0]
    minDistance = 2
    ok=False
    if(len(points)>0):
        for each in points:
            distance = math.sqrt((each[1] - direction[1]) ** 2 + (each[0] - direction[0]) ** 2)
            # distance=getDistancetoPoint(x1,y1,myX,mY)
            if (minDistance > distance):
                minDistance = distance
                direction_aux[0] = each[0]
                direction_aux[1] = each[1]
                ok=True
        if(ok==True):
            direction[0]=direction_aux[0]
            direction[1]=direction_aux[1]
    print(minDistance,direction)


def calibrate():
    global calibrationScreen
    global calibrationDirection
    global direction
    while (calibrationScreen == False or calibrationDirection==False):
        flags, hcursor, loc = win32gui.GetCursorInfo()
        printscreen, _ = grab_screen([0, 31, 720, 607])
        printscreen = cv2.circle(printscreen, (360, 323 - 31), 1, (0, 0, 255), 5)
        if(calibrationScreen==False):
            if cv2.waitKey(25) & 0xFF == ord('q'):
                calibrationScreen=True
                print("Screen has been calibrated")
        printscreen = cv2.circle(printscreen, (direction[0], direction[1] - 31), 1, (0, 255, 0 ), 5)
        if(calibrationDirection==False):
            direction[0]=loc[0]
            direction[1]=loc[1]
            if cv2.waitKey(25) & 0xFF == ord('w'):
                calibrationDirection = True
                print("Direction has been calibrated")
        cv2.imshow('calibration_window', printscreen)
    cv2.destroyAllWindows()
print("Calibration starting in 3 seconds")
for j in range(1):
    time.sleep(1)
    print(3-j)
calibrate()

for i in range(1):
    print('Program starting in:', 5-i,' seconds')
    time.sleep(1)


ok = 0
steps=0
while True:
    #flags, hcursor, (x, y) = win32gui.GetCursorInfo()
    printscreen, location = grab_screen([0, 31, 720, 607])
    #cv2.line(location, (360, 323-31), (360, 523-31), (255, 0, 0), 5)
    myX=360
    mY=323-31
    _, _, r , _= cv2.split(printscreen)
    #cv2.imshow('Rosu fara threshold',r)
    _, radar = cv2.threshold(r, 250, 255, cv2.THRESH_TOZERO)
    #cv2.imshow('Radar', radar)
    lines = cv2.HoughLinesP(radar, 2, np.pi / 180, 60, 1 , 100)
    points=[]
    try:
        for each in lines:
            coords=each[0]
            #print(coords)
            cv2.line(printscreen, (coords[0], coords[1]),(coords[2], coords[3]), (255, 0, 0), 4)

        targetX, targetY,distance,points = getClosestPoint(lines, myX, mY)
        update_direction(points)


        cv2.line(printscreen, (myX, mY),(int(targetX), int(targetY)) , (255, 0, 0), 5)
        cv2.line(printscreen, (myX,mY),(myX,mY-200),(0,255,0),5)
        next(targetX, targetY, myX, mY, distance)
        #cv2.line(location,(x11, y11),(x22, y22), (255, 0, 0), 10)
        #print(distance)

    except:
        pass

    # Deseneaza punctele folosite
    for each in points:
        location = cv2.circle(location, (int(each[0]), int(each[1])), 1, (255, 255, 255), 1)
    cv2.imshow('TARGET LINE', location)

    printscreen = cv2.circle(printscreen, (int(direction[0]), int(direction[1])), 1, (0, 255, 0), 5)
    cv2.imshow('Radar with lines', printscreen)


    #pt afisat mouse
    #print(flags, hcursor, (x, y))


    next(targetX=targetX,targetY=targetY,myX=myX,mY=mY,distance=distance)

    if(steps%100==0):
        print("Current distance:", distance)
    steps+=1

    #oprire
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break








