import math
import getshortestline
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4


def next(targetX,targetY,myX,mY,distance,distantafixa=200):
    pass
    #angle  =  get_angle(targetX=targetX, targetY=targetY,centerX=myX,centerY=mY,movementX=myX,movementY=mY-200,distanceA=distance,distanceB=distantafixa)
    #print(previousinput,previousAngle,angle)
    #print(angle)

#targetX,targetY,myX,mY,myX,my-200
#a=centru-linie
#b=centru-directie
#c=directie linie
def get_angle(targetX,targetY,centerX,centerY,movementX,movementY,distanceA,distanceB):
    a=distanceA
    b=distanceB
    c=getshortestline.getDistancetoPoint(targetX,targetY,movementX,movementY)
    angle=math.acos((a**2+b**2-c**2)/(2*a*b))
    angle=math.degrees(angle)
    return(angle)

def whichSide(targetX,myX,targetY,mY):
    #daca X e in stanga
    if(targetX<myX):
        return "sus"
    else:
        if(targetY<=mY):
            return "dreapta"
        else:
            return "stanga"

