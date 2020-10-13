import math
import time


def getslope(x1,y1,x2,y2):
    return((y2-y1)/(x2-x1))

def getDistance(x1,y1,x2,y2,pointX,pointY):
    #aflu panta liniei initiale
    slope = getslope(x1,y1,x2,y2)
    #calculez b ul
    b = -(slope * x1) + y1

    #calculez panta liniei perpendiculare
    negative_slope=-1/slope
    #cu ajutorul pantei aflu pe ce punct pe linie se intersecteaza
    intercept = -(negative_slope * pointX) + pointY
    x = (intercept - b)/slope

    #coordonatele punctului pe care pica perpendiculara
    interceptX = x
    interceptY = intercept

    distance = math.sqrt((interceptY-pointY)**2 + (interceptX-pointX)**2)

    online= checkOnLine(x1,y1,x2,y2,interceptX,interceptY)
    #print(x1,y1,x2,y2)
    return (interceptX,interceptY,distance,online)

def getClosestPoint(lines,myX,mY):
    minDistance=99999999
    targetX=myX
    targetY=mY
    for each in lines:
        online=False
        coords = each[0]
        tx,ty,distance,online = getDistance(coords[0], coords[1],coords[2], coords[3],myX,mY)

        if(minDistance>=distance):
            minDistance = distance
            targetX=tx
            targetY=ty
            x1=coords[0]
            y1=coords[1]
            x2=coords[2]
            y2=coords[3]


    return (targetX,targetY,minDistance,x1,y1,x2,y2)


def checkOnLine(x1,y1,x2,y2,interceptX,interceptY):
    slope=getslope(x1,y1,x2,y2)
    pt3_on = (interceptY - y1) == slope * (interceptX - x1)
    #print(pt3_on)
    return pt3_on
