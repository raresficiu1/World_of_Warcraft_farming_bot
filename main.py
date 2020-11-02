import cv2
import numpy as np
import win32gui, win32ui, win32con, win32api
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4
import time
from PIL import Image
from getshortestline import getClosestPoint
from nextStep import next
from pynput.mouse import Listener




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

def on_click(x, y, button, pressed):
    global direction
    if pressed:
        direction=(x,y)
        print ('Mouse clicked at ({0}, {1}) with {2}'.format(direction[0], direction[1], button))

calibration=False
direction=(0,0)
def calibrate():
    global calibration
    with Listener(on_click=on_click) as listener:
        while (calibration == False):
            printscreen, location = grab_screen([0, 31, 720, 607])
            printscreen = cv2.circle(printscreen, (360, 323 - 31), 1, (0, 0, 255), 5)
            printscreen = cv2.circle(printscreen, (direction[0], direction[1]-31), 1, (0, 255, 0), 5)
            cv2.imshow('window', printscreen)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                calibration = True
    listener.join()


for i in range(5):
    calibrate()
    print('Starting in:', 5-i,' seconds')
    time.sleep(1)



ok = 0
steps=0
previousAngle=180
previousinput=1
while True:
    flags, hcursor, (x, y) = win32gui.GetCursorInfo()
    printscreen, location = grab_screen([0, 31, 720, 607])
    #cv2.line(location, (360, 323-31), (360, 523-31), (255, 0, 0), 5)
    myX=360
    mY=323-31
    '''
    stanga = ((170, 120), (170, 470))
    jos = ((170, 470), (540, 470))
    dreapta = ((540, 120), (540, 470))
    sus = ((170, 120), (540, 120))
    lines=[]
    lines.append(stanga)
    lines.append(jos)
    lines.append(dreapta)
    lines.append(sus)
  '''
    # for each in lines:
    #     cv2.line(printscreen, each[0], each[1], (255, 0, 0), 5)

    #edges = cv2.Canny(printscreen, 100, 200)
    # cv2.imshow('edges', edges)
    #cv2.imshow('window', printscreen)

    #cv2.imshow('location', location)
    #crop_img = printscreen[120:470, 170:540]



    _, _, r , _= cv2.split(printscreen)

    #cv2.imshow('Rosu fara threshold',r)



    _, radar = cv2.threshold(r, 250, 255, cv2.THRESH_TOZERO)

    #cv2.imshow('Radar', radar)


    # _, folositor = cv2.threshold(crop_img, 127, 255, cv2.THRESH_TOZERO)
    # # thresh4 =cv2.cvtColor(thresh4, cv2.COLOR_BGR2GRAY)
    lines = cv2.HoughLinesP(radar, 2, np.pi / 180, 60, 10, 100)


    try:
        for each in lines:
            coords=each[0]
            #print(coords)
            cv2.line(printscreen, (coords[0], coords[1]),(coords[2], coords[3]), (255, 0, 0), 4)

        targetX, targetY,distance,points = getClosestPoint(lines, myX, mY)
        cv2.line(printscreen, (myX, mY),(int(targetX), int(targetY)) , (255, 0, 0), 5)
        cv2.line(printscreen, (myX,mY),(myX,mY-200),(0,255,0),5)
        next(targetX, targetY, myX, mY, distance)
        #cv2.line(location,(x11, y11),(x22, y22), (255, 0, 0), 10)
        #print(distance)
    except:
        pass


    #Deseneaza punctele folosite
    ''' for each in points:
        location = cv2.circle(location, (int(each[0]), int(each[1])), 1, (255, 255, 255), 1)
    cv2.imshow('TARGET LINE', location)
    '''


    cv2.imshow('Radar with lines', printscreen)


    #pt afisat mouse
    #print(flags, hcursor, (x, y))


    previousinput,previousAngle = next(targetX=targetX,targetY=targetY,myX=myX,mY=mY,distance=distance,previousAngle=previousAngle,previousinput=previousinput)

    if(steps%100==0):
        print("Current distance:", distance)
    steps+=1

    #oprire
    if cv2.waitKey(25) & 0xFF == ord('q'):
        ReleaseKey(W)
        ReleaseKey(numpad5)
        ReleaseKey(numpad4)
        cv2.destroyAllWindows()
        break









