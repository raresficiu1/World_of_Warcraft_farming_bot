import math
import time
import numpy as np

def getslope(x1,y1,x2,y2):

    if(abs(x1-x2)<1):
        return 'INF'
    return (y2-y1)/(x2-x1)


def getDistancetoLine(x1,y1,x2,y2,pointX,pointY):
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

def getDistancetoPoint(x1,y1,myX,mY):
    return(math.sqrt((y1 - mY) ** 2 + (x1 - myX) ** 2))

def getClosestPoint(lines,myX,mY):
    minDistance=99999
    targetX=myX
    targetY=mY
    points=[]
    for each in lines:
        coords = each[0]
        for each1 in getPoints(coords[0], coords[1],coords[2], coords[3]):
            points.append(each1)


    #print(len(points))
    for each in points:
        distance = math.sqrt((each[1] - mY) ** 2 + (each[0] - myX) ** 2)
        #distance=getDistancetoPoint(x1,y1,myX,mY)
        if(minDistance>distance):
            minDistance = distance
            targetX=each[0]
            targetY=each[1]

    return (targetX,targetY,minDistance,points)


def checkOnLine(x1,y1,x2,y2,interceptX,interceptY):
    slope=getslope(x1,y1,x2,y2)
    pt3_on = (interceptY - y1) == slope * (interceptX - x1)
    #print(pt3_on)
    return pt3_on

def getPoints(x1,y1,x2,y2):
    points=[]
    slope=getslope(x1,y1,x2,y2)
    if(slope!='INF'):
        b = -(slope * x1) + y1
        for x in np.arange(x1,x2,0.1):
            points.append((x,slope*x+b))
    else:
        if(y1>y2):
            for y in np.arange(y2,y1,0.1):
                points.append((x1,y))
        else:
            for y in np.arange(y1,y2,0.1):
                points.append((x1,y))

    return points


