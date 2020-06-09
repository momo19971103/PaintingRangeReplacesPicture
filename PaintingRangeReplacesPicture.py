import cv2
import numpy as np

# -----------------------鼠標操作相關------------------------------------------
lsPointsChoose = []
tpPointsChoose = []
pointsCount = 0
count = 0
pointsMax = 4
def on_mouse(event, x, y, flags, param):
    global img,imgTest, point1, point2, count, pointsMax
    global lsPointsChoose, tpPointsChoose  # 存入選擇的點
    global pointsCount  # 對鼠標按下的點計數
    global img2, ROI_bymouse_flag
    img2 = img.copy()  # 此行代碼保證每次都重新再原圖畫  避免畫多了
    # -----------------------------------------------------------
    #    count=count+1
    #    print("callback_count",count)
    # --------------------------------------------------------------

    if event == cv2.EVENT_LBUTTONDOWN:  # 左鍵點擊
        pointsCount = pointsCount + 1
        # 感覺這裏沒有用？2018年8月25日20:06:42
        # 爲了保存繪製的區域，畫的點稍晚清零
        # if (pointsCount == pointsMax + 1):
        #     pointsCount = 0
        #     tpPointsChoose = []
        print('pointsCount:', pointsCount)
        point1 = (x, y)
        print (x, y)
        # 畫出點擊的點
        cv2.circle(img2, point1, 10, (0, 255, 0), 2)

        # 將選取的點保存到list列表裏
        lsPointsChoose.append([x, y])  # 用於轉化爲array 提取多邊形ROI
        tpPointsChoose.append((x, y))  # 用於畫點
        # ----------------------------------------------------------------------
        # 將鼠標選的點用直線連起來
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        # ----------------------------------------------------------------------
        # ----------點擊到pointMax時可以提取去繪圖----------------
        if (pointsCount == pointsMax):
            # -----------繪製感興趣區域-----------
            ReplacePicture()
            #ROI_bymouse_flag = 1
            lsPointsChoose = []

        cv2.imshow('src', img2)
    # -------------------------右鍵按下清除軌跡-----------------------------
    if event == cv2.EVENT_RBUTTONDOWN:  # 右鍵點擊
        print("right-mouse")
        pointsCount = 0
        tpPointsChoose = []
        lsPointsChoose = []
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(img2, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        cv2.imshow('src', img2)

def ReplacePicture():
    nc2,nr2 = img.shape[:2]
    imgTnc2,imgTnr2 = imgTest.shape[:2]
    pts1 = np.float32([lsPointsChoose])
    ptsTest = np.float32([[0,0],[0,imgTnc2],[imgTnr2,imgTnc2],[imgTnr2,0]])
    T = cv2.getPerspectiveTransform(ptsTest,pts1)   ##cv2.getPerspectiveTransform(A,B)---取圖A範圍變為圖B
    ReplaceImg = cv2.warpPerspective(imgTest,T,(823,420))
    ###無縫融合參數
    
    imgTest_mask = np.zeros(imgTest.shape, imgTest.dtype)
    poly = np.array([lsPointsChoose], np.int32)
    cv2.fillPoly(imgTest_mask, [poly], (255, 255, 255))
    cv2.fillPoly(img, [poly], (200, 160, 200))
    X = (poly[0][0][0]+poly[0][1][0]+poly[0][2][0]+poly[0][3][0])//4
    Y = (poly[0][0][1]+poly[0][1][1]+poly[0][2][1]+poly[0][3][1])//4
    center = (X,Y)
    ###無縫融合參數
    output = cv2.seamlessClone(ReplaceImg, img, imgTest_mask, center, cv2.NORMAL_CLONE)#無縫融合
    cv2.imshow("Original img1 Image",img)
    cv2.imshow("Original imgTest Image",imgTest)
    cv2.imshow("Original Image",ReplaceImg)
    cv2.imshow("Perspective Transform",output)


def ROI_byMouse():
    global src, ROI, ROI_flag, mask2
    mask = np.zeros(img.shape, np.uint8)
    pts = np.array([lsPointsChoose], np.int32)  # pts是多邊形的頂點列表（頂點集）
    pts = pts.reshape((-1, 1, 2))
    # 這裏 reshape 的第一個參數爲-1, 表明這一維的長度是根據後面的維度的計算出來的。
    # OpenCV中需要先將多邊形的頂點座標變成頂點數×1×2維的矩陣，再來繪製

    # --------------畫多邊形---------------------
    mask = cv2.polylines(mask, [pts], True, (255, 255, 255))
    ##-------------填充多邊形---------------------
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
    cv2.imshow('mask', mask2)
    cv2.imwrite('mask.bmp', mask2)
    ROI = cv2.bitwise_and(mask2, img)
    cv2.imwrite('ROI.bmp', ROI)
    cv2.imshow('ROI', ROI)

imgTest = cv2.imread("2165001.bmp",-1)
img = cv2.imread('gallery.jpg')
# ---------------------------------------------------------
# --圖像預處理，設置其大小
# height, width = img.shape[:2]
# size = (int(width * 0.3), int(height * 0.3))
# img = cv2.resize(img, size, interpolation=cv2.INTER_AREA)
# ------------------------------------------------------------
ROI = img.copy()
cv2.namedWindow('src')
cv2.setMouseCallback('src', on_mouse)
cv2.imshow('src', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

##https://www.twblogs.net/a/5b8b46fc2b717718832e76f6##
