import cv2
import numpy as np

path = "Main_picture/Img_3.jpg"
img = cv2.imread(path)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
def empty(a):
    pass
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 255, 255, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

while True:
    ret,img = cap.read()
    imgBlur = cv2.GaussianBlur(img,(5,5),1)
    imgHsv = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    key = cv2.waitKey(30)
    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    kernel = np.ones((3, 3), np.uint16)
    pr_mask = cv2.dilate(mask, kernel, iterations= 1)
    result = cv2.bitwise_and(img, img, mask=pr_mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, result])
    cv2.imshow('Horizontal Stacking', hStack)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()