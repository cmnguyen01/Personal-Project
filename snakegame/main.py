
from ast import Continue
import math
import random
import cvzone
import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector
 
cap = cv2.VideoCapture(1)
cap.set(3, 1280)
cap.set(4, 720)
 
detector = HandDetector(detectionCon=0.8, maxHands=1)
vid = cv2.VideoCapture(0)
class snakeGame:
    def __init__(self):
        #point on the sname
        self.point=[]
        #snake length
        self.length=[]
        self.currentLength=0 #initial length
        #total length
        self.totalLength=150 
        self.previousHead=0,0
        self.life=0

    def update(self, imgMain, currentHead, life):
        self.life=life
        px, py=self.previousHead
        cx,cy=currentHead
        self.point.append([cx,cy])
        #get the distance
        distance=math.hypot(cx-px,cy-py)
        self.length.append(distance)
        self.currentLength+=distance
        #update previous head to previous current
        self.previousHead=cx,cy

        #length reduction
        if self.currentLength>self.totalLength:
            for i, length in enumerate(self.length):
                self.currentLength-=length
                self.length.pop(i)
                self.point.pop(i)
                if self.currentLength<self.totalLength:
                    break
        if self.point:
        #draw
            for i,points in enumerate(self.point):
            #cannot draw first point
                if i != 0:
                    cv2.line(imgMain,self.point[i-1],self.point[i],(0,0,255),20)
            cv2.circle(imgMain,self.point[-1],20,(200,0,200), cv2.FILLED)
        return imgMain    


game=snakeGame()
  
while(True):
      
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    frame=cv2.flip(frame,1)
    #detect hands, while flipping the identified hands to be correct
    hand, frame=detector.findHands(frame,flipType=False)
    # Display the resulting frame
    if hand:
        lmlist=hand[0]['lmList']
        #lmlist provides x,y,z values the second element is to restrict to 2 dimensions
        pointindex=lmlist[8][0:2]
        img=game.update(frame,pointindex,3)
        #cv2.circle(frame,pointindex,20,(200,0,200),cv2.FILLED)



    cv2.imshow('frame', frame)

    
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()