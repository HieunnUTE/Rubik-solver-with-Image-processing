import cv2
import numpy as np
# 5, 120, 20, 10, 255, 255 old orange
color_code = [
             [136, 87, 111, 180, 255, 255], # RED x
             [36, 100, 0, 100, 255, 255], # GREEN TEST x
             [94, 80, 2, 120, 255, 255], # BLUE x
             [0, 120, 0, 10, 170, 255], # ORANGE x
             [10, 80, 80, 60, 255, 255], # YELLOW x
             ]

color_name_list = ["r", "g", "b", "o", "y", "w"]

get_color = {
    "w": (255,255,255),
    "r": (0,0,255),
    "b": (255,0,0),
    "g": (0,255,0),
    "y": (0,255,255),
    "o": (51,170,255),
}
def config_webcam(camera_id = 0,width = 720, height = 480):
    """Hàm dùng để Config camera"""
    cap = cv2.VideoCapture(camera_id, cv2.CAP_DSHOW)
    cap.set(3, width)
    cap.set(4, height)
    return cap

def create_mask(imgHSV,color_code):
    """Hàm dùng để tạo mask cho các màu"""
    # HUE min, Val min, Value min
    lower = np.array(color_code[0:3])
    # HUE max, Val max, Value max
    upper = np.array(color_code[3:6])
    mask = cv2.inRange(imgHSV, lower, upper)
    return mask

def process_mask(mask):
    """Hàm xử dilate vật thể"""
    kernel = np.ones((3, 3), np.uint16)
    pr_mask = cv2.dilate(mask, kernel, iterations= 1)
    return pr_mask

def get_Contours(img, color_name = None, H = 1000):
    """Hàm này có nhiệm vụ tìm kiếm các vật thể có màu tương ứng với color_name"""
    contours,_ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) !=0:
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if ((H//3)**2)//9 <= area <= ((H//3)**2) :
                x, y, _, _ = cv2.boundingRect(cnt)
                if (x,y) != (0,0):
                    dictColor = {color_name:(x,y)}
                    return dictColor
                else:
                    pass
    else: pass

def get_miniROI(roi,W,H,x,y):
    """Hàm này dùng để tạo ra các mini_ROI"""
    miniROI = roi[y*(H//3):(y+1)*H//3,x*(W//3):(x+1)*W//3]
    return miniROI

# def get_miniROI_2faces(frame):
#     """Get 2 faces of rubik"""
#     roiFront = frame[135:375,165:321]
#     roiRight = frame[117:349,324:472]
#     return roiFront,roiRight

# def draw_2faces_rubik(frame):
#     shape = np.array([[165,135],[322,118],[475,135],[472,348],[323,374],[164,349]], np.int32)
#     shape = shape.reshape((-1,1,2))
#     cv2.polylines(frame,[shape],True,(255,255,255),2)
#     cv2.line(frame,(322,118),(323,374),(255,255,255),2)
#     return frame

def get_color_position(RoI,H):
    """Hàm chính kết hợp bởi 3 hàm con ở trên
    --> Trả về vị trí của các ô màu của Rubik trong RoI (Vùng chứa rubik)
    """
    index = 0
    imgBlur = cv2.GaussianBlur(RoI, (5,5), 1)
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)
    # Create a mask
    red_mask = create_mask(imgHSV, color_code[0])
    green_mask = create_mask(imgHSV, color_code[1])
    blue_mask = create_mask(imgHSV, color_code[2])
    orange_mask = create_mask(imgHSV, color_code[3])
    yellow_mask = create_mask(imgHSV, color_code[4])

    # # Process mask
    red_mask = process_mask(red_mask)
    green_mask = process_mask(green_mask)
    blue_mask = process_mask(blue_mask)
    orange_mask = process_mask(orange_mask)
    yellow_mask = process_mask(yellow_mask)

    # Find Color
    posR = get_Contours(red_mask, color_name = "r", H= H)
    posG = get_Contours(green_mask, color_name = "g", H= H)
    posB = get_Contours(blue_mask, color_name = "b", H= H)
    posO = get_Contours(orange_mask, color_name = "o", H= H)
    posY = get_Contours(yellow_mask, color_name = "y", H= H)

    # Process result
    result_list = [posR,posG,posB,posO,posY]
    result = np.where(np.array(result_list) != None)
    if len(result[0]) !=0:
        index = int(result[0][0])
        classColor = color_name_list[index]
        return classColor
    else: return None

