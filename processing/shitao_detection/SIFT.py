#coding=utf-8
import cv2
import time

sift = cv2.xfeatures2d.SIFT_create(nfeatures=1000)
img1 = cv2.imread("kong.jpg")
img2 = cv2.imread("tibaluokuan.jpg")
img3=img2
#img3=cv2.flip(img2,-1)
#求中心点，对图像进行旋转
#(h,w)=img2.shape[:2]
#center=(w//2,h//2)
#M=cv2.getRotationMatrix2D(center,30,1.0)
#img3=cv2.warpAffine(img2,M,(w,h))
#灰度化
img1_gray = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY)
img3_gray = cv2.cvtColor(img3, cv2.COLOR_RGB2GRAY)
kp1, des1 = sift.detectAndCompute(img1_gray, None)
kp2, des2 = sift.detectAndCompute(img3_gray, None)
#绘制特征点图
img1t=cv2.drawKeypoints(img1_gray,kp1,img1)
img3t=cv2.drawKeypoints(img3_gray,kp2,img3)
#进行KNN特征匹配，K设置为2
start=time.time()
bf = cv2.BFMatcher()
matches = bf.knnMatch(des1, des2, k=2)
good=[]
print(len(matches))
matchesMask = [[0, 0] for i in range(len(matches))]
for i, (m1, m2) in enumerate(matches):
    if m1.distance < 0.7* m2.distance:  # 两个特征向量之间的欧氏距离，越小表明匹配度越高。
        good.append(m1)
        matchesMask[i]=[1,0]
        pt1 = kp1[m1.queryIdx].pt  # queryIdx  是匹配之后所对应关键点的序号，第一个载入图片的匹配关键点序号
        pt2 = kp2[m1.trainIdx].pt  # trainIdx  是匹配之后所对应关键点的序号，第二个载入图片的匹配关键点序号
        #print(kpts1)
        print(i, pt1, pt2)   #打印匹配点个数，并标出两图中的坐标位置
        #画特征点及其周围的圆圈
        cv2.circle(img1, (int(pt1[0]), int(pt1[1])), 5, (0, 255, 0), -1)
        num = "{}".format(i)
        cv2.putText(img1, num, (int(pt1[0]), int(pt1[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
        cv2.circle(img3, (int(pt2[0]), int(pt2[1])), 5, (0, 255, 0), -1)
        cv2.putText(img3, num, (int(pt2[0]), int(pt2[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
end=time.time()
print("good match num:{} good match points:".format(len(good)))
print("number of feature points:", len(kp1), len(kp2))
#匹配连线
draw_params = dict(matchColor=(255, 0, 0),
                   singlePointColor=(0, 0, 255),
                   matchesMask=matchesMask,
                   flags=0)

res = cv2.drawMatchesKnn(img1, kp1, img3, kp2, matches, None,**draw_params)


print("运行时间:%.2f秒"%(end-start))
cv2.imshow("img1_gray",img1_gray)
cv2.imshow("img3_gray",img3_gray)
cv2.imshow("Result", res)
cv2.imshow("img1", img1)
cv2.imshow("img3", img3)
cv2.imwrite("SIFTimg1_gray.jpg",img1_gray)
cv2.imwrite("SIFTimg3_gray.jpg",img3_gray)
cv2.imwrite("SIFTimg1.jpg",img1)
cv2.imwrite("SIFTimg3.jpg",img3)
cv2.imwrite("SIFTimg1t.jpg",img1t)
cv2.imwrite("SIFTimg3t.jpg",img3t)
cv2.imwrite("SIFTResult.jpg",res)
cv2.waitKey(0)
#cv2.destroyAllWindows()

