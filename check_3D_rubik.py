import cv2
import numpy as np
from detect_color_off import *

font = cv2.FONT_HERSHEY_SIMPLEX

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

stateCurrent =  {
            'up':['r','y','b','y','y','r','y','b','w',],
            'left':['g','g','w','g','g','g','y','b','o',],
            'front':['o','y','o','w','r','o','b','g','b',],
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

def rotate(side):
    main=stateCurrent[side]
    front=stateCurrent['front']
    left=stateCurrent['left']
    right=stateCurrent['right']
    up=stateCurrent['up']
    down=stateCurrent['down']
    back=stateCurrent['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=down[0],down[1],down[2],left[8],left[5],left[2],up[6],up[7],up[8],right[6],right[3],right[0] 
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=front[0],front[1],front[2],left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8],left[6],left[7],left[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=up[2],up[1],up[0],right[2],right[5],right[8],down[8],down[7],down[6],left[0],left[3],left[6] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=up[0],up[3],up[6],front[0],front[3],front[6],down[6],down[3],down[0],back[8],back[5],back[2]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=down[2],down[5],down[8],back[6],back[3],back[0],up[8],up[5],up[2],front[2],front[5],front[8]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[6],main[3],main[0],main[7],main[4],main[1],main[8],main[5],main[2]

def revrotate(side):
    main=stateCurrent[side]
    front=stateCurrent['front']
    left=stateCurrent['left']
    right=stateCurrent['right']
    up=stateCurrent['up']
    down=stateCurrent['down']
    back=stateCurrent['back']
    
    if side=='front':
        left[2],left[5],left[8],up[6],up[7],up[8],right[0],right[3],right[6],down[0],down[1],down[2]=up[8],up[7],up[6],right[0],right[3],right[6],down[2],down[1],down[0],left[2],left[5],left[8]
    elif side=='up':
        left[0],left[1],left[2],back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2]=back[0],back[1],back[2],right[0],right[1],right[2],front[0],front[1],front[2],left[0],left[1],left[2]
    elif side=='down':
        left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8],front[6],front[7],front[8]=front[6],front[7],front[8],left[6],left[7],left[8],back[6],back[7],back[8],right[6],right[7],right[8]
    elif side=='back':
        left[0],left[3],left[6],up[0],up[1],up[2],right[2],right[5],right[8],down[6],down[7],down[8]=down[6],down[7],down[8],left[6],left[3],left[0],up[0],up[1],up[2],right[8],right[5],right[2] 
    elif side=='left':
        front[0],front[3],front[6],down[0],down[3],down[6],back[2],back[5],back[8],up[0],up[3],up[6]=down[0],down[3],down[6],back[8],back[5],back[2],up[0],up[3],up[6],front[0],front[3],front[6]
    elif side=='right':
        front[2],front[5],front[8],down[2],down[5],down[8],back[0],back[3],back[6],up[2],up[5],up[8]=up[2],up[5],up[8],front[2],front[5],front[8],down[8],down[5],down[2],back[6],back[3],back[0]

    main[0],main[1],main[2],main[3],main[4],main[5],main[6],main[7],main[8]=main[2],main[5],main[8],main[1],main[4],main[7],main[0],main[3],main[6]

def process(operation):
    replace={
                "F":[rotate,'front'],
                "F2":[rotate,'front','front'],
                "F'":[revrotate,'front'],
                "U":[rotate,'up'],
                "U2":[rotate,'up','up'],
                "U'":[revrotate,'up'],
                "L":[rotate,'left'],
                "L2":[rotate,'left','left'],
                "L'":[revrotate,'left'],
                "R":[rotate,'right'],
                "R2":[rotate,'right','right'],
                "R'":[revrotate,'right'],
                "D":[rotate,'down'],
                "D2":[rotate,'down','down'],
                "D'":[revrotate,'down'],
                "B":[rotate,'back'],
                "B2":[rotate,'back','back'],
                "B'":[revrotate,'back']           
    }    
    a=0
    for i in operation:
        x = str(i)
        for j in range(len(replace[x])-1):
            replace[x][0](replace[x][j+1])
            cv2.putText(sovleFrame, x, (700,a+50), font,1,(0,255,0), 1, cv2.LINE_AA)  
            fill_3D_rubik(sovleFrame,rubik,stateCurrent)
            
            cv2.imshow("Sovle Step",sovleFrame)
            cv2.waitKey()

sovleFrame = np.zeros((480, 640, 3), dtype= np.uint8)

def draw_3D_rubik(sovleFrame,rubik):
    stick=['up','front','right',] #Y #R #G
    for name in stick:
        if name == 'up':
            for x,y in rubik[name]:
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

def fill_3D_rubik(sovleFrame,rubik,stateCurrent):
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

sovleFrame = draw_3D_rubik(sovleFrame,rubik)
sovleFrame = fill_3D_rubik(sovleFrame,rubik,stateCurrent)
solve_step = solve_rubik("rybyyrybwyrgbbowrooyowrobgbggwgggyborogyowyrgwwrbworwb")
print(solve_step)
process(solve_step)
# cv2.imshow("Result",sovleFrame)
cv2.waitKey(0)