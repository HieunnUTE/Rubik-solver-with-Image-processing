from offline_process import *
import os
import time
import numpy as np
from rubik_solver import utils
from rubik.cube import Cube
""" FILE này lấy hình ảnh từ file Main_picture để xử lý
    Hàm main() sẽ là hàm xử lý chính --> Nhiệm vụ: return matrix 
"""

def matrix_color(ROI,colorList = []):
    """Hàm có nhiệm vụ nhận đầu vào là 1 ROI (vùng chứ rubik)
    --> Trả về 1 matrix tương ứng với vị trí các màu của 1 mặt trong rubik
    """
    # Khởi tạo các var cần thiết để tạo Matrix Color
    x,y=0,0     # Vị trí element color trong rubik
    (H, W) = ROI.shape[:2]  # Kích thước của ROI
    stringColor = ''    # Xử lý để trả về đúng format của thư viện Cube
    # Vì rubik có 9 ô màu --> Tạo vòng lặp để thực hiện cho từng ô
    for i in range(9):
        # Khởi tạo từng mini ROI với các vị trí tương ứng là x,y -- cột,hàng
        miniROI = get_miniROI(ROI,W,H,x,y)

        # Sau khi tạo ra MiniROI>coi như là hình ảnh --> Đưa vào để tìm ra màu sắc
        # Lưu ý: Vì mỗi ô chỉ được có thể chứa 1 màu duy nhất
        # --> Đòi hỏi phải config rubik đúng hình ROI đã vẽ
        classColor = get_color_position(miniROI,H)  # --> Trả về màu sắc tại vị trí ô màu
        
        # Nếu không xác định được màu tại ô đó --> Trả về màu trắng -- white
        # Trong process function chỉ tạo mask cho [r,b,g,y,o] --> 5 màu
        if classColor == None: classColor = "w"

        # Sau khi đã có được màu: kí tự kí hiệu -- "r",hay "b", hay ...
        # Dịch tiếp sang ô tiếp theo (theo cột) --> sang phải
        # Add màu đó vào colorList -- Xem như là ma trận màu của Rubik
        x+=1 ; colorList.append(classColor[0].lower())
        # Thêm kí tự đó vào stringColor --> trả về đúng format của Cube
        stringColor +=str(classColor[0]).lower()

        # Thêm các điều kiện để tiếp tục vòng lặp
        if x==3:
            y+=1; x = 0
        if y==3: break
    return colorList,stringColor


def solve_rubik(stateColor,levels = None):
    """Hàm này nhận đầu vào là stateColor
    Nhược điểm: Chỉ mới config được đúng format của pp "Kociemba"
    --> Return List: gồm các bước giải rubik"""
    stateColor = stateColor.lower()
    if levels == None: levels = "Kociemba"
    solve_step = utils.solve(stateColor, levels)
    return solve_step

