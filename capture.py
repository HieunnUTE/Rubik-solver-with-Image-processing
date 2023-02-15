import cv2
cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
if not cap.isOpened:
   print('Cant open camera')
   exit(0)
cap.set(3,480)
cap.set(4,720)
cnt = 80
path = "Main_picture/"
ret,frame = cap.read()
H,W,_ = frame.shape
while True:
    ret,frame = cap.read()
    cv2.circle(frame,(W//2,H//2),5,(0,255,0),-1)
    key = cv2.waitKey(30)
    if ret:
        if key == ord("s"):
            cv2.imwrite(f"{path}Img_{cnt}.jpg",frame)
            cnt += 1
    
    # Nhấn ESC hoặc q để thoát   
    cv2.imshow("Result",frame)
    if key == 27 or key == ord("q"): break

cap.release()
cv2.destroyAllWindows