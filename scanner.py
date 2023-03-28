import cv2
import numpy as np
import mapper
image=cv2.imread("images/WhatsApp Image 2023-03-16 at 20.51.46 (3).jpeg")   #read in the image
image=cv2.resize(image,(1300,800)) #resizing because opencv does not work well with bigger images
orig=image.copy()

gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)  #RGB To Gray Scale
cv2.imshow("Title",gray)
cv2.waitKey(0)


# blurred=cv2.GaussianBlur(gray,(5,5),0)  #(5,5) is the kernel size and 0 is sigma that determines the amount of blur
# cv2.imshow("Blur",blurred)
# cv2.waitKey(0)


edged=cv2.Canny(gray,250,260)  #30 MinThreshold and 50 is the MaxThreshold
cv2.imshow("Canny",edged)
cv2.waitKey(0)

contours,hierarchy=cv2.findContours(edged,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)  #retrieve the contours as a list, with simple apprximation model
contours=sorted(contours,key=cv2.contourArea,reverse=True)

#the loop extracts the boundary contours of the page
for c in contours:
    p=cv2.arcLength(c,True)
    approx=cv2.approxPolyDP(c,0.02*p,True)

    if len(approx)==4:
        target=approx
        break
approx=mapper.mapp(target) #find endpoints of the sheet

pts=np.float32([[0,0],[800,0],[800,800],[0,800]])  #map to 800*800 target window

op=cv2.getPerspectiveTransform(approx,pts)  #get the top or bird eye view effect
dst=cv2.warpPerspective(orig,op,(800,800))


cv2.imshow("Scanned",dst)
cv2.imwrite("Scanned.jpg", dst)
# press q or Esc to close
cv2.waitKey(0)
cv2.destroyAllWindows()