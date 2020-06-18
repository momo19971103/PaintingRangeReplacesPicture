import cv2
import numpy as np

# -----------------------鼠標操作相關------------------------------------------
lsPointsChoose = []
tpPointsChoose = []
pointsCount = 0
count = 0
pointsMax = 4
def on_mouse(event, x, y, flags, param):
    global galleryImg,replaceImg, clickPoint, count, pointsMax
    global lsPointsChoose, tpPointsChoose  # 存入選擇的點
    global pointsCount  # 對鼠標按下的點計數
    global copyImg
    copyImg = galleryImg.copy()  # 此行代碼保證每次都重新再原圖畫  避免畫多了
    # -----------------------------------------------------------
    #    count=count+1
    #    print("callback_count",count)
    # --------------------------------------------------------------

    if event == cv2.EVENT_LBUTTONDOWN:  # 左鍵點擊
        pointsCount = pointsCount + 1
        print('pointsCount:', pointsCount)
        clickPoint = (x, y)
        print (x, y)
        # 畫出點擊的點
        cv2.circle(copyImg, clickPoint, 10, (0, 255, 0), 2)

        # 將選取的點保存到list列表裏
        lsPointsChoose.append([x, y])  # 用於轉化爲array 提取多邊形ROI
        tpPointsChoose.append((x, y))  # 用於畫點
        # ----------------------------------------------------------------------
        # 將鼠標選的點用直線連起來
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(copyImg, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        # ----------------------------------------------------------------------
        # ----------點擊到pointMax時可以提取去繪圖----------------
        if (pointsCount == pointsMax):
            # -----------繪製感興趣區域-----------
            ReplacePicture()
            lsPointsChoose = []

        cv2.imshow('src', copyImg)
    # -------------------------右鍵按下清除軌跡-----------------------------
    if event == cv2.EVENT_RBUTTONDOWN:  # 右鍵點擊
        print("right-mouse")
        pointsCount = 0
        tpPointsChoose = []
        lsPointsChoose = []
        print(len(tpPointsChoose))
        for i in range(len(tpPointsChoose) - 1):
            print('i', i)
            cv2.line(copyImg, tpPointsChoose[i], tpPointsChoose[i + 1], (0, 0, 255), 2)
        cv2.imshow('src', copyImg)

def ReplacePicture():
    nc2,nr2 = galleryImg.shape[:2]
    imgTnc2,imgTnr2 = replaceImg.shape[:2]
    pts1 = np.float32([lsPointsChoose])
    ptsTest = np.float32([[0,0],[0,imgTnc2],[imgTnr2,imgTnc2],[imgTnr2,0]])
    T = cv2.getPerspectiveTransform(ptsTest,pts1)   ##cv2.getPerspectiveTransform(A,B)---取圖A範圍變為圖B
    ReplaceImg = cv2.warpPerspective(replaceImg,T,(823,420))
    ###無縫融合參數
    
    imgTest_mask = np.zeros(replaceImg.shape, replaceImg.dtype)
    poly = np.array([lsPointsChoose], np.int32)
    cv2.fillPoly(imgTest_mask, [poly], (255, 255, 255))
    cv2.fillPoly(galleryImg, [poly], (200, 160, 200))
    X = (poly[0][0][0]+poly[0][1][0]+poly[0][2][0]+poly[0][3][0])//4
    Y = (poly[0][0][1]+poly[0][1][1]+poly[0][2][1]+poly[0][3][1])//4
    center = (X,Y)
    ###無縫融合參數
    output = cv2.seamlessClone(ReplaceImg, galleryImg, imgTest_mask, center, cv2.NORMAL_CLONE)#無縫融合
    cv2.imshow("Original img1 Image",galleryImg)
    cv2.imshow("Original imgTest Image",replaceImg)
    cv2.imshow("Original Image",ReplaceImg)
    cv2.imshow("Perspective Transform",output)


replaceImg = cv2.imread("2165001.bmp",-1)
galleryImg = cv2.imread('gallery.jpg')
cv2.namedWindow('src')
cv2.setMouseCallback('src', on_mouse)
cv2.imshow('src', galleryImg)
cv2.waitKey(0)
cv2.destroyAllWindows()

