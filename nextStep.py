import math
import getshortestline
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4

def next(targetX,targetY,myX,mY,distance,distantafixa=200):
    pass

    #print(previousinput,previousAngle,angle)qw
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


def get_angle2(currentX,currentY,targetX,targetY):
    #punctu meu
    x1=currentX
    y1=currentY
    #punctu ala
    x2=currentX
    y2=currentY-100
    #tot eu
    x3=currentX
    y3=currentY
    #targetu  mancatias
    x4=targetX
    y4=targetY
    nr=((x2-x1)*(x4-x3)+(y2-y1)*(y4-y3))/((math.sqrt((x2-x1)**2+(y2-y1)**2))*(math.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)))
    try:
        result=math.acos(nr)
        #result=math.degrees(result)
    except Exception as e:
        print(e)
        result='ERROR'

    return(result)

def whichSide(targetX,myX,targetY,mY):
    #daca X e in stanga
    if(targetX<myX):
        return "sus"
    else:
        if(targetY<=mY):
            return "dreapta"
        else:
            return "stanga"

