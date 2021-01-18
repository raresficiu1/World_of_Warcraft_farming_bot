import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4
import time
from PIL import Image
from getshortestline import getClosestPoint,getDistancetoPoint
from nextStep import next,get_angle2
from pynput.mouse import Listener
import math

#Values
calibrationScreen=False
calibrationDirection=False
direction=[0,0]
initialX=360
initialY=323-31
currentX=360
currentY=323-31
r=125
HMin=23
HMax=23
VMin=201
VMax=255
SMin=227
SMax=255

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

    img.shape = (height, width, 4)


    srcdc.DeleteDC()
    memdc.DeleteDC()
    win32gui.ReleaseDC(hwin, hwindc)
    win32gui.DeleteObject(bmp.GetHandle())

    return img

def init_control_gui():
    global HMin, HMax, VMin, VMax, SMin, SMax
    window = cv2.namedWindow('window',cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window,350,700)
    def nothing(position):
        pass
    cv2.createTrackbar('HMin', 'window', 0, 179, nothing)
    cv2.createTrackbar('HMax', 'window', 0, 179, nothing)
    cv2.createTrackbar('SMin', 'window', 0, 255, nothing)
    cv2.createTrackbar('SMax', 'window', 0, 255, nothing)
    cv2.createTrackbar('VMin', 'window', 0, 255, nothing)
    cv2.createTrackbar('VMax','window', 0, 255, nothing)

    cv2.setTrackbarPos('HMin', 'window', HMin)
    cv2.setTrackbarPos('SMin', 'window', SMin)
    cv2.setTrackbarPos('VMin', 'window', VMin)
    cv2.setTrackbarPos('HMax','window',HMax)
    cv2.setTrackbarPos('SMax','window',SMax)
    cv2.setTrackbarPos('VMax', 'window', VMax)


def get_filters_from_panel():
    global HMin,HMax,VMin,VMax,SMin,SMax
    HMin = cv2.getTrackbarPos('HMin','window')
    HMax = cv2.getTrackbarPos('HMax', 'window')
    VMin = cv2.getTrackbarPos('VMin', 'window')
    VMax = cv2.getTrackbarPos('VMax','window')
    SMin = cv2.getTrackbarPos('SMin', 'window')
    SMax = cv2.getTrackbarPos('SMax', 'window')

def HSVFILTER(original_image):
    global HMin, HMax, VMin, VMax, SMin, SMax
    frame_HSV = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

    frame_threshold = cv2.inRange(frame_HSV, (HMin, SMin, VMin), (HMax, SMax, VMax))

    aux= np.zeros((250,250,3))
    aux[0:250,0:250,1]=frame_threshold[initialY-r:initialY+r,initialX-r:initialX+r]
    aux[0:250, 0:250, 0] = frame_threshold[initialY-r:initialY+r,initialX-r:initialX+r]
    aux[0:250, 0:250, 2] = frame_threshold[initialY-r:initialY+r,initialX-r:initialX+r]


    #aux = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    return(aux)

def update_direction(points):
    global direction
    allowedDistance = 100
    bestPointsFromCenter=[]
    realdistance=0
    bestPoint =[0,0]
    bestPoint[0]= direction[0]
    bestPoint[1]= direction[1]
    # gasesc punctele cele mai apropiate de distanta 175 de pe linie
    if (len(points) > 0):
        ok=0
        for each in points:
            x1 = each[0]
            y1 = each[1]
            distance = getDistancetoPoint(x1, y1, currentX, currentY)
            realdistance=abs(allowedDistance-distance)

            if(realdistance<5):
                ok=1
                bestPointsFromCenter.append([x1,y1])
        #gasesc punctele cele mai apropiate de vechea directie

        if(ok==1):
            bestPoint=[]
            bestdistanceFromPrevious=9999
            for each in bestPointsFromCenter:
                x1 = each[0]
                y1 = each[1]

                distance = getDistancetoPoint(x1, y1, direction[0], direction[1])

                if(distance<bestdistanceFromPrevious):
                    bestdistanceFromPrevious=distance
                    bestPoint=[x1,y1]
        direction[0] = bestPoint[0]
        direction[1] = bestPoint[1]




#Functia initiala de calibrare
def calibrate():
    global calibrationScreen
    global calibrationDirection
    global direction
    pressed=False
    while (calibrationScreen == False or calibrationDirection==False):
        flags, hcursor, loc = win32gui.GetCursorInfo()
        printscreen= grab_screen([0, 31, 720, 607])
        printscreen = cv2.circle(printscreen, (currentX, currentY), 1, (0, 0, 255), 5)
        if(calibrationScreen==False):
            if cv2.waitKey(25) & 0xFF == ord('q'):
                calibrationScreen=True
                print("Screen has been calibrated")
        #print(getDistancetoPoint(direction[0],direction[1],currentX,currentY))
        #print(getDistancetoPoint(loc[0],loc[1],currentX,currentY))
        printscreen = cv2.circle(printscreen, (direction[0], direction[1]), 1, (0, 255, 0 ), 5)
        if(calibrationDirection==False):
            direction[0]=loc[0]
            direction[1]=loc[1]-31
            if cv2.waitKey(25) & 0xFF == ord('w'):
                calibrationDirection = True
                print("Direction has been calibrated")

        if cv2.waitKey(25) & 0xFF == ord('k'):
            pressed=True
            init_control_gui()

        if(pressed):
            get_filters_from_panel()
            cv2.imshow('calibration_window2', HSVFILTER(printscreen))
        else:
            cv2.imshow('calibration_window', printscreen)

    cv2.destroyAllWindows()


#De bagat in main START
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
currentX=int(r)
currentY=int(r)

kp=0.5
ki=0.01
kd=0
sum_error=0
previous_error=1
current_error=1
v=0.001

while True:
    '''PressKey(W)
    ReleaseKey(numpad4)
    ReleaseKey(numpad5)'''
    printscreen = grab_screen([0, 31, 720, 607])  #printscreen
    printscreen = printscreen[initialY-r:initialY+r,initialX-r:initialX+r]#decupez
    blank = np.zeros((2*r,2*r))
    blank2 = np.zeros((2*r,2*r))
    ###Threshold
    #pt linie
    _, g, _ , _= cv2.split(printscreen)
    _, radar = cv2.threshold(g, 254, 255, cv2.THRESH_TOZERO)
    cv2.imshow('Radar', radar)


    #pt ore
    # The order of the colors is blue, green, red
    oreuri = HSVFILTER(printscreen)
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(oreuri)

    blank4 = cv2.drawKeypoints(oreuri, keypoints, np.array([]), (0, 0, 255),
                                         cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv2.imshow('TARGET', oreuri)
    cv2.imshow('TARGET_IN',blank4)


    #scot liniile
    lines = cv2.HoughLinesP(radar, rho=1, theta= np.pi / 180,threshold= 10, minLineLength=12 ,maxLineGap= 70)
    points=[]
    try:
        for each in lines:
            coords=each[0]
            #print(coords)
            cv2.line(blank2, (coords[0], coords[1]),(coords[2], coords[3]), (255, 0, 0), 4)

        targetX, targetY,distance,points = getClosestPoint(lines, currentX, currentY)

        update_direction(points)

        cv2.line(printscreen, (currentX, currentY),(int(targetX), int(targetY)) , (255, 0, 0), 5)
        cv2.line(printscreen, (currentX,currentY),(currentX,currentY-100),(0,255,0),5)
        cv2.line(printscreen, (currentX, currentY), (int(direction[0]), int(direction[1])), (255, 255, 255), 5)
        next(targetX, targetY, currentX, currentY, distance)

    except Exception as e:
        print(e)


    # Deseneaza punctele folosite
    '''for each in points:
        blank = cv2.circle(blank, (int(each[0]), int(each[1])), 1, (255, 0, 0),1)'''


    angle = get_angle2(currentX,currentY,direction[0],direction[1])
    previous_error = current_error
    current_error = angle
    #stanga
    if(current_error)>0.09:
        if(currentX<direction[0]):
            sum_error=sum_error-distance
            try:
                u=current_error*kp+sum_error*ki+(current_error/previous_error)*kd
            except:
                u = current_error * kp + sum_error * ki

            #PressKey(numpad5)
            #time.sleep(v*abs(u))
            #ReleaseKey(numpad5)
        elif currentX>direction[0]:
            sum_error = sum_error + distance
            try:
                u = current_error * kp + sum_error * ki + (current_error / previous_error) * kd
            except:
                u = current_error * kp + sum_error * ki

            #PressKey(numpad4)
            #time.sleep(v * abs(u))
            #ReleaseKey(numpad4)
        #print("U=", u, 'current_error',current_error,'sum_error',sum_error)

    #cv2.imshow('Linii', blank2)
    #cv2.imshow('Puncte scoase', blank)
    update_direction(points)
    #print(direction[0],direction[1])
    printscreen = cv2.circle(printscreen, (int(direction[0]), int(direction[1])), 1, (255, 0, 255), 5)
    printscreen = cv2.circle(printscreen, (currentX, currentY), 1, (0, 0, 255), 5)
    cv2.imshow('Radar with lines', printscreen)


    if(steps%600==0):
        print("Current distance:", distance)
    steps+=1
    #oprire
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break


#flags, hcursor, (x, y) = win32gui.GetCursorInfo()
#pt afisat mouse
#print(flags, hcursor, (x, y))
