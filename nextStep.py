import math
import getshortestline
from directkeys import PressKey, ReleaseKey, W,numpad5,numpad4


def next(targetX,targetY,myX,mY,distance,previousAngle,previousinput,distantafixa=200):

    angle  =  get_angle(targetX=targetX, targetY=targetY,centerX=myX,centerY=mY,movementX=myX,movementY=mY-200,distanceA=distance,distanceB=distantafixa)
    #print(previousinput,previousAngle,angle)
    print(previousAngle,angle)

    if (angle <= 90 or distance < 10):
        PressKey(W)
        ReleaseKey(numpad4)
        ReleaseKey(numpad5)
    else:
        if(angle>150):
            strongPressKey(numpad5)
            return(1,angle)
        else:
            ReleaseKey(W)
            ReleaseKey(numpad4)
            ReleaseKey(numpad5)
            #case in which the left failed to bring the angle closer to 90
            if(previousinput == 0 and angle >= previousAngle):
                ReleaseKey(numpad4)
                PressKey(numpad5)
                print("D")
                return( 1, angle)
            else:
                ReleaseKey(numpad5)
                PressKey(numpad4)
                print("A")
                return(0 ,angle)

            #case in which the right failed to bring the angle closer to 90
            if(previousinput==1 and angle>=previousAngle):
                ReleaseKey(numpad5)
                PressKey(numpad4)
                print("A")
                return (0, angle)
            else:
                ReleaseKey(numpad4)
                PressKey(numpad5)
                print("D")
                return (1, angle)

    return previousAngle,previousinput

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

