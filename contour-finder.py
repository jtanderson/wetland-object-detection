import matplotlib, cv2
import numpy as np
import matplotlib.pyplot as plt

#%matplotlib inline

# load the image
image = cv2.imread("MicasenseImagesPanels/IMG_0075_2.tif", 1)
imgray = cv2.imread("MicasenseImagesPanels/IMG_0075_2.tif", 0)
#imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
im2, contours, hiearchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

print(image)

# red color boundaries [B, G, R]
lower = [1, 0, 20]
upper = [60, 40, 200]

# create NumPy arrays from the boundaries
lower = np.array(lower, dtype="uint8")
upper = np.array(upper, dtype="uint8")

# find the colors within the specified boundaries and apply
# the mask
mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=mask)

ret,thresh = cv2.threshold(mask, 40, 255, 0)
im2,contours,hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

if len(contours) != 0:
    # draw in blue the contours that were founded
    cv2.drawContours(output, contours, -1, 255, 3)

    #find the biggest area
    c = max(contours, key = cv2.contourArea)

    x,y,w,h = cv2.boundingRect(c)
    # draw the book contour (in green)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

# show the images
cv2.imshow("Result", np.hstack([image, output]))


cv2.waitKey(0)



#coins = cv2.imread('cat.jpg')
# create copy of image to draw bounding boxes
#bounding_img = np.copy(coins)

# for each contour find bounding box and draw rectangle
#for contour in large_contours:
#    x, y, w, h = cv2.boundingRect(contour)
#    cv2.rectangle(bounding_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

#plt.imshow(cv2.cvtColor(bounding_img, cv2.COLOR_BGR2RGB))
#cv2.imwrite('output/coins-bounding.jpg', bounding_img)