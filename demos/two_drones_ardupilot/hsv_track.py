# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import cv2,sys
import numpy as np

def find_red(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv,(130,130,180),(255,255,255))
    mask = cv2.erode(mask, np.ones((2,1)) , iterations=1)
    mask = cv2.dilate(mask, None, iterations=3)
    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    frame=img.copy()    
    ###based on example from  http://www.pyimagesearch.com/2015/09/14/ball-tracking-with-opencv
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 3:
            cv2.circle(frame, (int(x), int(y)), 12,(0, 255, 255), 2)
    return frame

if __name__=='__main__':
    cnt=0
    while 1:
        print(cnt)
        img=cv2.imread(r'/tmp/drone_images0/img%06d.png'%cnt)
        frame=find_red(img)
        cv2.imshow('img',frame)
        cv2.waitKey(0)
        cnt+=1
