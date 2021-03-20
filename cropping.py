import cv2

# 画像読み込み
img = cv2.imread("./assets/ranking_number.jpg")

# No1
img1 = img[0 : 227, 0: 227]
cv2.imwrite("assets/no1.jpg", img1)
# No2
img2 = img[0 : 227, 343 : 343 + 227]
cv2.imwrite("assets/no2.jpg", img2)
# No3
img3 = img[0 : 227, 343 + 343 : 343 + 343 + 227]
cv2.imwrite("assets/no3.jpg", img3)