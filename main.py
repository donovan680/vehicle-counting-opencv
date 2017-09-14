import cv2
import numpy as np

cap = cv2.VideoCapture('traffic.avi')

#Create the background subtractor
fgbg = cv2.createBackgroundSubtractorMOG2(detectShadows = False)

kernelOp = np.ones((3,3), np.uint8)
kernelCl = np.ones((11,11), np.uint8)

font = 
areaTH = 500

while(cap.isOpened()):
    #read a frame
    ret, frame = cap.read()

    fgmask = fgbg.apply(frame)

    try:
        #cv2.imshow('Frame', frame)
        #cv2.imshow('Backgroud Subtraction', fgmask)
        ret, imBin = cv2.threshold(fgmask, 200, 255, cv2.THRESH_OTSU)
        #Opening (erode->dilate)
        mask = cv2.morphologyEx(imBin, cv2.MORPH_OPEN, kernelOp)
        #Closing (dilate->erode)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernelCl)
        cv2.imshow('Image Threshold', imBin)
        cv2.imshow('Masked Image', mask)
    except:
        #If there is no more frames to show...
        print('EOF')
        break

    _, contours0, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for cnt in contours0:
        cv2.drawContours(frame, cnt, -1, (0,255,0), 3, 8)
        area = cv2.contourArea(cnt)
        print area
        if area > areaTH:
            ################
            #   TRACKING   #
            ################
            M = cv2.moments(cnt)
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            x,y,w,h = cv2.boundingRect(cnt)
            
            new = True
            
            cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
            img = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow('Frame', frame)
    #cv2.imshow('Backgroud Subtraction', fgmask)

    #Abort and exit with 'Q' or ESC
    k = cv2.waitKey(50) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
