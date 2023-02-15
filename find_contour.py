import cv2
import numpy as np
from offline_process import *
from detect_color_off import *
def empty(a):
    pass

cv2.namedWindow('Contours')
thresh1=150
thresh2=250
cv2.createTrackbar('thresh1','Contours', thresh1, 1000,empty)
cv2.createTrackbar('thresh2','Contours', thresh2, 1000,empty)
cap = config_webcam(camera_id = 1,width = 720, height = 480)
while True:
    ret,frame = cap.read()
    org = frame.copy()
    if not ret: break
    if frame is None:
        print('No captured frame, Break!')
        break
    key = cv2.waitKey(30)
    kernel = (3,5)
    thresh1 = cv2.getTrackbarPos('thresh1', 'Contours')
    thresh2 = cv2.getTrackbarPos('thresh2', 'Contours')
    
    imgGray = cv2.cvtColor(org,cv2.COLOR_BGR2GRAY)               
    blurred = cv2.GaussianBlur(imgGray, kernel, 1)
    kernel = np.ones((3, 3), np.uint16)
    imgCloseGauss = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel,50)
    imgOpenGauss = cv2.morphologyEx(imgCloseGauss, cv2.MORPH_OPEN, kernel,50)
    edged = cv2.Canny(imgOpenGauss, thresh1, thresh2)
    # img_contours = np.zeros(frame.shape)
    cv2.imshow("Test",edged)
    
    contours,_ = cv2.findContours(edged, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    list_cor = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 1000 <= area:
            x, y, w, h = cv2.boundingRect(cnt)
            roi = frame[y:y+w-5,x:x+w-5]
            print(roi.shape)
            # cv2.circle(frame,(int(x),int(y)),5,(255,0,0),-1)
            # cv2.circle(frame,(int(x+w),int(y+w)),5,(255,0,0),-1)
            # cv2.rectangle(frame,(int(x),int(y)),(int(x+w),int(y+w)),(255,0,0),2)
            if (180,180,3) <= roi.shape <= (260,260,3):
                cv2.imshow("Frame",roi)
    if key == ord("q"):
        break
