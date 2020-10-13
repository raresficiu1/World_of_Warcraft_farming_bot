import math
import getshortestline
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4


def next(targetX,targetY,myX,mY,distance,previousAngle,previousinput,distantafixa=200):

        angle  =  get_angle(targetX=targetX, targetY=targetY,centerX=myX,centerY=mY,movementX=myX,movementY=mY-200,distanceA=distance,distanceB=distantafixa)
        #print(previousinput,previousAngle,angle)
        if(previousinput==True or previousinput==False):
            print("ALELUIA")

        if (angle <= 90 or distance < 10):
            PressKey(W)
            ReleaseKey(numpad4)
            ReleaseKey(numpad5)
        else:
            ReleaseKey(W)
            ReleaseKey(numpad4)
            ReleaseKey(numpad5)
            #case in which the left failed to bring the angle closer to 90
            if(previousinput == False and angle > previousAngle):
                ReleaseKey(numpad4)
                PressKey(numpad5)
                print("D")
                return(True , angle)
            else:
                ReleaseKey(numpad5)
                PressKey(numpad4)
                print("A")
                return(False ,angle)

            #case in which the right failed to bring the angle closer to 90
            if(previousinput==True and angle>previousAngle):
                ReleaseKey(numpad5)
                PressKey(numpad4)
                print("A")
                return (False, angle)
            else:
                ReleaseKey(numpad4)
                PressKey(numpad5)
                print("D")
                return (True, angle)

        return previousAngle,previousinput

#targetX,targetY,myX,mY,myX,my-200
#a=centru-linie
#b=centru-directie
#c=directie linie
def get_angle(targetX,targetY,centerX,centerY,movementX,movementY,distanceA,distanceB):
    a=distanceA
    b=distanceB
    c=getshortestline.getDistancetoPoint(targetX,targetY,movementX,movementY)
    try:
        angle=math.acos((a**2+b**2-c**2)/(2*a*b))
        angle=math.degrees(angle)
        return(angle)
    except:
        return 100

def whichSide(targetX,myX,targetY,mY):
    #daca X e in stanga
    if(targetX<myX):
        return "sus"
    else:
        if(targetY<=mY):
            return "dreapta"
        else:
            return "stanga"


def get_next_to_press(steps):
    stanga=steps.count("stanga")
    dreapta=steps.count("dreapta")
    if(stanga>=dreapta):
        return "dreapta"
    if(dreapta>=stanga):
        return "stanga"