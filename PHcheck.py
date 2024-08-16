import cv2
import numpy as np
import os
import argparse
parser = argparse.ArgumentParser(description="根据图像测量PH值")

# 添加参数
parser.add_argument('--image_path', type=str, help="待检测图像路径")
parser.add_argument('--ROI', type=bool, default=False, help="是否检测ROI区域")
parser.add_argument('--fit', type=int, default=3, help="拟合强度")
parser.add_argument('--true', type=str, default="./imageSource/", help="ground truth path")
# 解析参数
args = parser.parse_args()
x =[]
y =[]
def getROI(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_color = np.array([20, 43, 46])
    upper_color = np.array([124, 255, 255])    
    mask = cv2.inRange(hsv, lower_color, upper_color)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    arlph = 0.07
    for contour in contours:
        # 计算轮廓的面积并忽略小面积
        area = cv2.contourArea(contour)
        if area > 2000:  # 设定一个合适的阈值
            # 获取轮廓的边界框
            x, y, w, h = cv2.boundingRect(contour)
            if float(w) / h <0.6:
                image = image[int(y+y*(arlph+0.05)):int(y+h-y*(arlph)),int(x+x*arlph):int(x+w-x*arlph)]
                return image
for imageName in sorted(os.listdir(args.true)):
    if ".jpg" in imageName and "+" not in imageName:
        image = cv2.imread(args.true+imageName)
        image = getROI(image)
        HSV_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        image_B = HSV_image[:,:,0]/ (gray_image+0.001)
        x.append(image_B.mean())
        y.append(float(imageName[:-4]))

coefficients = np.polyfit(x,y,args.fit)
ploy = np.poly1d(coefficients)

image = cv2.imread(args.image_path)
if args.ROI:
    image = getROI(image)
    cv2.imwrite("ROI.jpg",image)
HSV_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
image_B = HSV_image[:,:,0]/ (gray_image+0.001)
x_fit = image_B.mean()
y_fit = ploy(x_fit)
y_fit = "{:.1f}".format(y_fit)
print("测试图像名称:",args.image_path.split("/")[-1][:-4],"本次PH测试结果为:",y_fit,"请检查ROI图片是否正确")



x = [3.223603530109218,
2.526641400252664,
2.2129597673176926,
1.9028618621807987,
1.790417905800731,
1.4010912027955889,
1.003389336656669,
0.767527483587769,
0.24875250618149974,
0.11525729346569527,
0.028569387900864225,
0.8770559253356663]
y = [
    1,2,3,4,5,6,7,8,9,10,11,12
]
