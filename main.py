from detect_color_off import *
from offline_process import *
from imutils.video import FPS

cap = config_webcam(camera_id = 1,width = 720, height = 480) #720 #480

if not cap.isOpened:
   print('Cant open camera') 
   exit(0)


path = "Main_picture/"
ret,frame = cap.read()
H,W,_ = frame.shape

font = cv2.FONT_HERSHEY_SIMPLEX

preview_frame = np.zeros((700, 800, 3), dtype = np.uint8)

sovleFrame = np.zeros((480, 640, 3), dtype= np.uint8)

stt = ['up','left','front','right','back','down',]

clr_num = ['Yellow','Blue','Red','Green','Orange','White',]

count,wrong,loop,faces = True,0,5,0
condition_list = []

# Tạo 1 biến để lưu các trạng thái màu của các mặt
stateCurrent =  {
            'up':['w','w','w','w','y','w','w','w','w',],
            'left':['w','w','w','w','b','w','w','w','w',],
            'front':['w','w','w','w','r','w','w','w','w',],
            'right':['w','w','w','w','g','w','w','w','w',],
            'back':['w','w','w','w','o','w','w','w','w',],
            'down':['w','w','w','w','w','w','w','w','w',],
            }

color = {
        'r'    : (0,0,255),
        'o' : (0,165,255),
        'b'   : (255,0,0),
        'g'  : (0,255,0),
        'w'  : (255,255,255),
        'y' : (0,255,255)
        }

# Vị trí của các ô màu dạng 2D
stickers = {
        'main': [
            [200, 120], [300, 120], [400, 120],
            [200, 220], [300, 220], [400, 220],
            [200, 320], [300, 320], [400, 320]
        ],
        'current': [
            [20, 20], [54, 20], [88, 20],
            [20, 54], [54, 54], [88, 54],
            [20, 88], [54, 88], [88, 88]
        ],
        'preview': [
            [20, 130], [54, 130], [88, 130],
            [20, 164], [54, 164], [88, 164],
            [20, 198], [54, 198], [88, 198]
        ],
        'left': [
            [50, 280], [94, 280], [138, 280],
            [50, 324], [94, 324], [138, 324],
            [50, 368], [94, 368], [138, 368]
        ],
        'front': [
            [188, 280], [232, 280], [276, 280],
            [188, 324], [232, 324], [276, 324],
            [188, 368], [232, 368], [276, 368]
        ],
        'right': [
            [326, 280], [370, 280], [414, 280],
            [326, 324], [370, 324], [414, 324],
            [326, 368], [370, 368], [414, 368]
        ],
        'up': [
            [188, 128], [232, 128], [276, 128],
            [188, 172], [232, 172], [276, 172],
            [188, 216], [232, 216], [276, 216]
        ],
        'down': [
            [188, 434], [232, 434], [276, 434],
            [188, 478], [232, 478], [276, 478],
            [188, 522], [232, 522], [276, 522]
        ], 
        'back': [
            [464, 280], [508, 280], [552, 280],
            [464, 324], [508, 324], [552, 324],
            [464, 368], [508, 368], [552, 368]
        ],
           }

# Vị trí các cell màu dạng 3D
rubik = {
        "front": [
                [138, 158],  [194, 183],  [250, 208],
                [138, 208],  [194, 233],  [250, 258],
                [138, 258],  [194, 283],  [250, 308],
                ],
        "up": [

                [300,81],   [356,106],  [412,131],
                [244,106],  [300,131],  [354,156],
                [188,131],  [244,156],  [300,181],
                ],
        "right":[
                [305,228],  [361,204],  [417,178],
                [305,278],  [361,254],  [417,228],
                [305,328],  [361,303],  [417,278],
                ],
        }

def draw_preview_stickers(preview_frame,stickers):
    """Hàm này dùng để vẽ ra các ô màu trắng"""
    stick=['front','back','left','right','up','down']
    for name in stick:
        for x,y in stickers[name]:
            preview_frame = cv2.rectangle(preview_frame, (x,y), (x+40, y+40), (255,255,255), 2) 
    return preview_frame

def draw_3D_rubik(sovleFrame,rubik):
    """Hàm này dùng để vẽ ra Rubik dưới dạng 3D: Up face - Front Face - RightFace"""
    stick=['up','front','right',] #Y #R #G

    # Đối với các mặt khác nhau sẽ có cách vẽ khác nhau
    for name in stick:
        if name == 'up':
            for x,y in rubik[name]:
                # Vẽ ô trong rubik theo thứ tự các cạnh
                # Topleft - Topright - Botright - Botleft
                shapeU = np.array([[x,y],[x+49,y+20],[x+2,y+40],[x-47,y+19]], np.int32)
                shapeU = shapeU.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeU],True,(255,255,255),2)
        elif name == 'front':
            for x,y in rubik[name]:
                shapeF = np.array([[x,y],[x+46,y+20],[x+46,y+60],[x,y+40]], np.int32)
                shapeF = shapeF.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeF],True,(255,255,255),2)
        elif name == 'right':
            for x,y in rubik[name]:
                shapeR = np.array([[x,y],[x+46,y-20],[x+46,y+21],[x,y+42]], np.int32)
                shapeR = shapeR.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeR],True,(255,255,255),2)
    return sovleFrame

def fill_stickers(preview_frame,stickers,stateCurrent):
    """Hàm này dùng để cập nhật trạng thái màu từ StateCurrent
    sau đó update (vẽ lên trên các ô trắng đã vẽ từ hàm draw_sticker) = màu tương ứng
    """ 
    for side,colors in stateCurrent.items():
        num=0
        for x,y in stickers[side]:
            preview_frame = cv2.rectangle(preview_frame,(x,y),(x+40,y+40),color[colors[num]],-1)
            num+=1
    return preview_frame

def fill_3D_rubik(sovleFrame,rubik,stateCurrent):
    """Hàm này dùng để cập nhật trạng thái màu từ StateCurrent --> vẽ lên 3D rubik"""
    for side,colors in stateCurrent.items():
        num=0
        if side == 'front':
            for x,y in rubik[side]:
                shapeF = np.array([[x,y],[x+46,y+20],[x+46,y+60],[x,y+40]], np.int32)
                shapeF = shapeF.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeF],True,color[colors[num]],2)
                num+=1
        elif side == 'up':
            for x,y in rubik[side]:
                shapeU = np.array([[x,y],[x+49,y+20],[x+2,y+40],[x-47,y+19]], np.int32)
                shapeU = shapeU.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeU],True,color[colors[num]],2)
                num+=1
        elif side == 'right':
            for x,y in rubik[side]:
                shapeR = np.array([[x,y],[x+46,y-20],[x+46,y+21],[x,y+42]], np.int32)
                shapeR = shapeR.reshape((-1,1,2))
                cv2.polylines(sovleFrame,[shapeR],True,color[colors[num]],2)
                num+=1
        else:
            pass
    return sovleFrame

def show_guide(faces,imgShow):
    """Hàm này dùng để vẽ ra các hướng dẫn trên frame để lấy dữ liệu"""
    if faces == 0:
        cv2.putText(imgShow, "Put Yellow Center", (255,430), font, 0.8 ,
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
        if loop % 5:
            cv2.arrowedLine(imgShow, (W//2+250,H//2), (W//2+150,H//2),
                                        color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2+250,H//2-100), (W//2+150,H//2-100),
                                        color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2+250,H//2+100), (W//2+150,H//2+100),
                                        color[clr_num[faces].lower()[0]], 3)

            cv2.arrowedLine(imgShow, (W//2-250,H//2), (W//2-150,H//2),
                                        color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2-250,H//2-100), (W//2-150,H//2-100),
                                        color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2-250,H//2+100), (W//2-150,H//2+100),
                                        color[clr_num[faces].lower()[0]], 3)
    if faces == 1:
        cv2.putText(imgShow, "B1: Turn Down", (W//2+180,H//2-50), font, 0.8 ,
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
        if loop % 5:
            cv2.arrowedLine(imgShow, (485,125), (485,360),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.putText(imgShow, "B2: Turn Left", (255,430), font, 0.8 ,
                            color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
            cv2.arrowedLine(imgShow, (440,400), (200,400),
                                    color[clr_num[faces].lower()[0]], 3)
    elif 2 <= faces <5:
        cv2.putText(imgShow, "Turn Right", (255,430), font, 0.8 ,
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
        if loop % 5:
            cv2.arrowedLine(imgShow, (W//2-250,H//2), (W//2-150,H//2),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2-250,H//2-100), (W//2-150,H//2-100),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2-250,H//2+100), (W//2-150,H//2+100),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow,(W//2+150,H//2), (W//2+250,H//2), 
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow,(W//2+150,H//2-100), (W//2+250,H//2-100), 
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2+150,H//2+100),(W//2+250,H//2+100), 
                                    color[clr_num[faces].lower()[0]], 3)
    elif faces == 5:
        cv2.putText(imgShow, "B1: Turn Left x2 to RED", (255,430), font, 0.8 ,
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
        cv2.putText(imgShow, "B2: Turn Down", (10,135), font, 0.8 ,
                            color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)
        if loop % 5:
            cv2.arrowedLine(imgShow, (W//2+250,H//2), (W//2+150,H//2),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2+250,H//2-100), (W//2+150,H//2-100),
                                    color[clr_num[faces].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (W//2+250,H//2+100), (W//2+150,H//2+100),
                                    color[clr_num[faces].lower()[0]], 3)
            
            cv2.arrowedLine(imgShow, (150,125), (150,360),
                                    color[clr_num[faces].lower()[0]], 3)
    
    elif faces > 5:
        cv2.putText(imgShow, "B1: Turn Up to RED", (255,430), font, 0.8 ,
                        color[clr_num[faces-1].lower()[0]], 2, cv2.LINE_AA)
        cv2.putText(imgShow, "B2: Press Q to solve", (40,30), font, 0.8 ,
                        color[clr_num[faces-1].lower()[0]], 2, cv2.LINE_AA)
        if loop % 5:
            cv2.arrowedLine(imgShow, (485,360), (485,125),
                                    color[clr_num[faces-1].lower()[0]], 3)
            cv2.arrowedLine(imgShow, (150,360),(150,125),
                                    color[clr_num[faces-1].lower()[0]], 3)

"""Hàm xử lý trạng thái màu của rubik --> cập nhật màu cho stateCurrent"""
def rotate(side):
    
    main=stateCurrent[side]
    front=stateCurrent['front']
    left=stateCurrent['left']
    right=stateCurrent['right']
    up=stateCurrent['up']
    down=stateCurrent['down']
    back=stateCurrent['back']
    
    if side=='front':
        left[2],left[5],left[8], up[6],up[7],up[8], right[0],right[3],right[6], down[0],down[1],down[2] = down[0], down[1], down[2] ,left[2], left[5], left[8], up[6], up[7], up[8], right[6], right[3], right[0]
        front[0], front[1], front[2], front[3], front[4], front[5], front[6], front[7], front[8] = front[6], front[3], front[0], front[7], front[4], front[1], front[8], front[5], front[2]
    
    elif side=='up':
        left[0], left[1], left[2] ,back[0],back[1],back[2], right[0],right[1],right[2], front[0],front[1],front[2] = front[0], front[1], front[2], left[0],left[1],left[2], back[0],back[1],back[2],right[0],right[1],right[2]
        up[0], up[1], up[2], up[3], up[4], up[5], up[6], up[7], up[8] = up[6], up[3], up[0], up[7], up[4], up[1], up[8], up[5], up[2]
    
    elif side=='down':
        right[6],right[7],right[8], back[6],back[7],back[8], left[6],left[7],left[8], front[6],front[7],front[8] = front[6],front[7],front[8], right[6],right[7],right[8], back[6],back[7],back[8], left[6],left[7],left[8]
        down[0], down[1], down[2], down[3], down[4], down[5], down[6], down[7], down[8] = down[6], down[3], down[0], down[7], down[4], down[1], down[8], down[5], down[2]      

    elif side=='back':
        left[0],left[3],left[6], up[0],up[1],up[2], right[2],right[5],right[8], down[6],down[7],down[8] = up[2],up[1],up[0], right[2],right[5],right[8], down[8],down[7],down[6], left[0],left[3],left[6]
        back[0], back[1], back[2], back[3], back[4], back[5], back[6], back[7], back[8] = back[6], back[3], back[0], back[7], back[4], back[1], back[8], back[5], back[2] 
    
    elif side=='left':
        front[0],front[3],front[6], down[0],down[3],down[6], back[2],back[5],back[8], up[0],up[3],up[6] = up[0],up[3],up[6], front[0],front[3],front[6], down[6],down[3],down[0], back[8],back[5],back[2]
        left[0], left[1], left[2], left[3], left[4], left[5], left[6], left[7], left[8] = left[6], left[3], left[0], left[7], left[4], left[1], left[8], left[5], left[2] 
    
    elif side=='right':
        front[2],front[5],front[8], down[2],down[5],down[8], back[0],back[3],back[6], up[2],up[5],up[8] = down[2],down[5],down[8], back[6],back[3],back[0], up[8],up[5],up[2], front[2],front[5],front[8]
        right[0], right[1], right[2], right[3], right[4], right[5], right[6], right[7], right[8] = right[6], right[3], right[0], right[7], right[4], right[1], right[8], right[5], right[2]


def revrotate(side):
    main=stateCurrent[side]
    front=stateCurrent['front']
    left=stateCurrent['left']
    right=stateCurrent['right']
    up=stateCurrent['up']
    down=stateCurrent['down']
    back=stateCurrent['back']
    
    if side=='front':
        left[2],left[5],left[8], up[6],up[7],up[8], right[0],right[3],right[6], down[0],down[1],down[2] = up[8],up[7],up[6], right[0],right[3],right[6], down[2],down[1],down[0], left[2],left[5],left[8]
        front[0],front[1],front[2],front[3],front[4],front[5],front[6],front[7],front[8]=front[2],front[5],front[8],front[1],front[4],front[7],front[0],front[3],front[6]
    
    elif side=='up':
        left[0],left[1],left[2], back[0],back[1],back[2], right[0],right[1],right[2], front[0],front[1],front[2] = back[0],back[1],back[2], right[0],right[1],right[2], front[0],front[1],front[2], left[0],left[1],left[2]
        up[0],up[1],up[2],up[3],up[4],up[5],up[6],up[7],up[8]=up[2],up[5],up[8],up[1],up[4],up[7],up[0],up[3],up[6]
    
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=front[6],front[7],front[8],left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8]
        down[0],down[1],down[2],down[3],down[4],down[5],down[6],down[7],down[8]=down[2],down[5],down[8],down[1],down[4],down[7],down[0],down[3],down[6]
    
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=down[6],down[7],down[8],left[6],left[3],left[0],up[0],up[1],up[2],right[8],right[5],right[2] 
        back[0],back[1],back[2],back[3],back[4],back[5],back[6],back[7],back[8] = back[2],back[5],back[8],back[1],back[4],back[7],back[0],back[3],back[6]
    
    elif side=='left':
        front[0],front[3],front[6], down[0],down[3],down[6], back[2],back[5],back[8], up[0],up[3],up[6] = down[0],down[3],down[6], back[8],back[5],back[2], up[6],up[3],up[0], front[0],front[3],front[6]
        left[0],left[1],left[2],left[3],left[4],left[5],left[6],left[7],left[8] = left[2],left[5],left[8],left[1],left[4],left[7],left[0],left[3],left[6]
    
    elif side=='right':
        front[2],front[5],front[8], down[2],down[5],down[8], back[0],back[3],back[6], up[2],up[5],up[8] = up[2],up[5],up[8], front[2],front[5],front[8], down[8],down[5],down[2], back[6],back[3],back[0]
        right[0],right[1],right[2],right[3],right[4],right[5],right[6],right[7],right[8] = right[2],right[5],right[8],right[1],right[4],right[7],right[0],right[3],right[6]
    
replace={
                "F":[rotate,"rotate",'front'],
                "F2":[rotate,"rotate",'front','front'],
                "F'":[revrotate,"revrotate",'front'],
                "U":[rotate,"rotate",'up'],
                "U2":[rotate,"rotate",'up','up'],
                "U'":[revrotate,"revrotate",'up'],
                "L":[rotate,"rotate",'left'],
                "L2":[rotate,"rotate",'left','left'],
                "L'":[revrotate,"revrotate",'left'],
                "R":[rotate,"rotate",'right'],
                "R2":[rotate,"rotate",'right','right'],
                "R'":[revrotate,"revrotate",'right'],
                "D":[rotate,"rotate",'down'],
                "D2":[rotate,"rotate",'down','down'],
                "D'":[revrotate,"revrotate",'down'],
                "B":[rotate,"rotate",'back'],
                "B2":[rotate,"rotate",'back','back'],
                "B'":[revrotate,"revrotate",'back']           
    }

def show_step(imgSovleFrame,direct,side,j):
    """ Hàm này dùng để vẽ ra các hướng trên 3D rubik nhằm chỉ dẫn hướng"""
    arrow = {
        "front" : [[182,148] , [294,199], [322,239], [322,342],],
        "back" : [[438,288], [438,186], [408,147], [296,99]],
        "up": [[438,186], [322,239], [267,239], [152,186],],
        "down": [[152,287],[267,342],[322,342], [438,288],],
        "left": [[296,99], [183,148], [152,186], [152,287],],
        "right": [[267,342], [267,239], [294,199] ,[408,147],],
    }
    # Sẽ có 2 trạng thái của mũi tên: Thuận: rotate && Nghịch: rerotate
    if direct == "rotate":
        s1,e1,s2,e2= arrow[side][0],arrow[side][1],arrow[side][2],arrow[side][3]
    else:
        s1,e1,s2,e2= arrow[side][3],arrow[side][2],arrow[side][1],arrow[side][0]

    # Thay đổi trạng thái màu của mũi tên
    if j % 2: color1 = (255,255,255); color2  = (0,0,255)
    else: color1 = (155,155,255); color2 = (255,255,255)
    # Vẽ mũi tên lên Frame
    cv2.arrowedLine(imgSovleFrame, s1, e1, color1, 3)
    cv2.arrowedLine(imgSovleFrame, s2, e2, color2, 3)
    return imgSovleFrame

def show_arrow(center,imgShow,direct,side,colorListFront):
    if center > (50,50): x,y = center
    else: x,y = (-200,-200)
    arrow_2D = {
        "up":       [(x+204,y+40),(x+44,y+40)],
        "front":    [(x+44,y+120), (x+124,y+40),(x+204,y+120),(x+124,y+200)],
        "back":     [(x+44,y+5),(x+204,y+5),(x+44,y+80),(x+204,y+80),(x+44,y+155) ,(x+204,y+155)],
        "down":     [(x+44,y+190),(x+204,y+190)],
        "left":     [(x+44,y+40),(x+44,y+200)],
        "right":    [(x+190,y+200),(x+190,y+40)]
    }
    if side != "return":
        if direct == "rotate":
            if side == "front":
                s1,e1,e2,e3 = arrow_2D[side][0],arrow_2D[side][1],arrow_2D[side][2],arrow_2D[side][3]
            elif side == "back":
                s1,e1,s2,e2,s3,e3 = arrow_2D[side][0],arrow_2D[side][1],arrow_2D[side][2],arrow_2D[side][3],arrow_2D[side][4],arrow_2D[side][5]
                s11,e11 = arrow_2D["right"][0],arrow_2D["right"][1]
            else:
                s1,e1 = arrow_2D[side][0],arrow_2D[side][1]

        else:
            if side == "front":
                e3,e2,e1,s1 = arrow_2D[side][0],arrow_2D[side][1],arrow_2D[side][2],arrow_2D[side][3]
            elif side == "back":
                s1,e1,s2,e2,s3,e3 = arrow_2D[side][0],arrow_2D[side][1],arrow_2D[side][2],arrow_2D[side][3],arrow_2D[side][4],arrow_2D[side][5]
                e11,s11 = arrow_2D["right"][0],arrow_2D["right"][1]

            else:
                e1,s1 = arrow_2D[side][0],arrow_2D[side][1]
    
    if side == "front":
        cv2.arrowedLine(imgShow, s1, e1, (0,255,0), 4)
        cv2.arrowedLine(imgShow, e1, e2, (0,255,0), 4)
        cv2.arrowedLine(imgShow, e2, e3, (0,255,0), 4)
        cv2.arrowedLine(imgShow, e3, s1, (0,255,0), 4)
    elif side == "back":
        if colorListFront[4] == "r":
            cv2.arrowedLine(imgShow, s1, e1, (0,255,0), 4)
            cv2.arrowedLine(imgShow, s2, e2, (0,255,0), 4)
            cv2.arrowedLine(imgShow, s3, e3, (0,255,0), 4)
        elif colorListFront[4] == "g":
            cv2.arrowedLine(imgShow, s11, e11, (0,255,0), 4)

    elif side == "return":
        s1,e1,s2,e2,s3,e3 = arrow_2D["back"][0],arrow_2D["back"][1],arrow_2D["back"][2],arrow_2D["back"][3],arrow_2D["back"][4],arrow_2D["back"][5]
        cv2.arrowedLine(imgShow, e1, s1, (0,255,0), 4)
        cv2.arrowedLine(imgShow, e2, s2, (0,255,0), 4)
        cv2.arrowedLine(imgShow, e3, s3, (0,255,0), 4)

    else:
        cv2.arrowedLine(imgShow, s1, e1, (0,255,0), 4)
    return imgShow

def find_rubik(frame):
    kernel = (5,5)  
    blurred = cv2.GaussianBlur(frame, kernel, 1)
    # kernel = np.ones((3, 3), np.uint16)
    # imgCloseGauss = cv2.morphologyEx(blurred, cv2.MORPH_CLOSE, kernel,50)
    # imgOpenGauss = cv2.morphologyEx(imgCloseGauss, cv2.MORPH_OPEN, kernel,50)
    edged = cv2.Canny(blurred, 50, 250)
    contours,_ = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    roi,center = None,(-10,-10)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        
        if 9000 <= area <= 21000:
            x, y, w, h = cv2.boundingRect(cnt)
            if 0.9 <= w/h <= 1.1 and 0.9 <= h/w <= 1.1:
                roi = frame[y:y+w-5,x:x+w-5]
                if (200,200,3) <= roi.shape <= (250,250,3):
                    center = x,y
    return roi,center
            
# Thêm điều kiện dừng:
a = ['r','r','r','r','r','r','r','r','r']
b = ['g','g','g','g','g','g','g','g','g']

stateColor = ''
if __name__=='__main__':
    while True:
        # Kiểm tra và check webcam
        ret,frame = cap.read()
        if not ret: break
        if frame is None:
            print('No captured frame, Break!')
            break
        

        # Copy Frame --> show KQ mà không ảnh hưởng đến Frame
        imgShow = frame.copy()
        key = cv2.waitKey(30)

        # Đưa ra hướng dẫn để lấy dữ liệu của 6 mặt
        if faces<6:
            cv2.putText(imgShow, f"{stt[faces].title()} Face", (130,90), font, 1 , 
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)

            cv2.putText(imgShow, f"{clr_num[faces]} Center", (350,90), font, 1 , 
                        color[clr_num[faces].lower()[0]], 2, cv2.LINE_AA)

        if faces <=5:
            roi,center = find_rubik(frame)
            if roi is not None:
                colorList,stringColor = matrix_color(roi,colorList = [])
                if colorList[4] == stateCurrent[stt[faces]][4]:
                    stateCurrent[stt[faces]]=colorList
                    stateColor +=stringColor
                    if faces <= 5: faces+=1

                            #     condition_list.append(colorList)
                            #     if len(condition_list) == 2:
                            #         if np.all([cond == condition_list[-1] for cond in condition_list]):
                            #             stateCurrent[stt[faces]]=colorList
                            #             stateColor +=stringColor
                            #             if faces <= 5: faces+=1
                            #         condition_list = []
                            # else: condition_list = []

        if key == 27 or key == ord("q"): break
        elif key == ord("b") and faces !=0: 
            faces-=1; stateColor = stateColor.replace(stateColor[-9:],"")
            stateCurrent[stt[faces]] = ['w','w','w','w',stateCurrent[stt[faces]][4],'w','w','w','w',]
        preview_frame = draw_preview_stickers(preview_frame,stickers)
        preview_frame = fill_stickers(preview_frame,stickers,stateCurrent)
        sovleFrame = draw_3D_rubik(sovleFrame,rubik)
        sovleFrame = fill_3D_rubik(sovleFrame,rubik,stateCurrent)
        loop +=1
        cv2.imshow("Collect Face Rubik",imgShow)
        cv2.imshow("Preview",preview_frame)
    cv2.destroyAllWindows()

    # Hiện KQ trạng thái màu của Rubik sau khi đã thực hiện lấy dữ liệu
    cv2.putText(sovleFrame.copy(), "Press Any Key to Begin", (50,50), font, 0.7 , 
                        (0,255,255), 2, cv2.LINE_AA)
    cv2.imshow("3D Rebik Preview", sovleFrame.copy())
    cv2.imshow("2D Rubik Preview", preview_frame)
    cv2.waitKey(0)
    
    print("Press Any Key to Begin")
    cv2.destroyAllWindows()
    # Thêm điều kiện ràng buộc: Cần phải chụp đủ 6l --> Giải
    if faces == 6:
        # Gọi hàm xử lý --> return color_list + stateColor của rubik
        print(stateColor)
        print("Rubik Solving ~~~")

        # Vì sẽ rất dễ gặp lỗi trong qtrinh giải
        try:
            solve_step = solve_rubik(stateColor)
            print(f"Step solve Rubik Cube: {solve_step}")
            try:
                step,j = 0,1
                old_state = stateCurrent
                x = str(solve_step[step])
                # Init Fps
                fps = FPS().start()
                while True:
                    # Tiến hành tương tự như trên
                    ret,framer = cap.read()
                    imgShow = framer.copy()
                    # Tương tự gọi hàm để xử lý và lấy màu
                    roiFront,center = find_rubik(framer)
                    if roiFront is not None:
                        colorListFront,_ = matrix_color(roiFront,colorList= [])

                        if x[0] != "B" and colorListFront[4] == "g":
                            imgShow = show_arrow(center,imgShow,replace[x][1],"return",colorListFront)
                        # Hiện hướng dẫn bằng lời nói đối với TH oay nhiều lần
                        else:
                            imgSovleFrame = cv2.putText(sovleFrame.copy(), f"{str(replace[x][1].title())} {str(replace[x][j+1].title())} {str(len(replace[x])-2)} Time", (300,50), font, 0.7 ,(255,255,255), 1, cv2.LINE_AA)
                            # Gọi hàm show_step để vẽ mũi tên lên 3D rubik
                            
                            imgSovleFrame = show_step(imgSovleFrame.copy(),replace[x][1],replace[x][j+1],j)
                            imgShow = show_arrow(center,imgShow,replace[x][1],replace[x][j+1],colorListFront)

                        if stateCurrent['front'] == colorListFront and x[0] != "B":
                            if step >= len(solve_step): print("Done"); break
                            old_state = stateCurrent
                            x = str(solve_step[step])
                            replace[x][0](replace[x][j+1])
                            if j < len(replace[x])-2:
                                j+=1
                            else:
                                step +=1
                                fill_3D_rubik(sovleFrame,rubik,old_state)
                                fill_stickers(preview_frame,stickers,old_state)
                                j = 1

                        elif stateCurrent['right'] == colorListFront and x[0] == "B":
                            if step >= len(solve_step): print("Done"); break
                            old_state = stateCurrent
                            x = str(solve_step[step])
                            replace[x][0](replace[x][j+1])
                            if j < len(replace[x])-2:
                                j+=1
                            else:
                                step +=1
                                fill_3D_rubik(sovleFrame,rubik,old_state)
                                fill_stickers(preview_frame,stickers,old_state)
                                j = 1
                        cv2.imshow("Sovle Step",imgSovleFrame)
                            
                    fps.update()
                    fps.stop()
                    cv2.putText(imgShow, str(np.round(fps.fps(),2)), (7, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (150, 250, 0), 3, cv2.LINE_AA)
                    key = cv2.waitKey(30)
                    cv2.imshow("Config Rubik",imgShow)
                    if key == 27 or key == ord("q"): break
            except:
                    print("\nSomething went wrong")
            
        except:
            print("\nEROR: in side detection ,you may do not follow sequence or some color not detected well.Try again! PLEASE!")
            solve_step = []
        
    else:
        print(f"\nSides not scanned! Remaining: {6-faces} Faces")
        print("Check all these side please!")
        print(stt[faces:])

