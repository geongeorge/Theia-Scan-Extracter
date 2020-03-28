from PIL import Image,ImageFilter
import cv2 
import os
import numpy as np
# import numpy as np

def _openImage(im):
    return Image.open(im)

def processImage(im,thresh):
    img = _openImage(im)
    # garyscale
    img = img.convert('L')
    gray = img
    # threshold
    threshold = thresh
    gray = gray.point(lambda p: p > threshold and 255) 

    # filter - noise
    gray = gray.filter(ImageFilter.MedianFilter(3)) 

    # pix = np.array(img)
    
    # otsuPix = otsu(pix)

    # img.putdata(otsuPix)
    return gray


def showImage(img,showSample=False):
    thresh = ~np.array(img)  # also invert
    thresh_img = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    contours,hierarchy = findCountours(thresh)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        # crop and save
        if(w>=50 and h >= 50):
            # Ouput single characters files
            if(showSample):
                cv2.rectangle(thresh_img,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(thresh_img, str(w)+","+str(h), (x, y), cv2.FONT_HERSHEY_SIMPLEX , 2, (0,255, 0),3 )
        #Add Recty
    pilImg = Image.fromarray(thresh_img)
    pilImg.show()

def findCountours(thresh):
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    # if split, then split
    # RETR_EXTERNAL only external contours
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    return contours,hierarchy

def saveImage(img,split=False,fl="output.jpg"):
    img.save(fl)

    if(not split):
        return


    thresh = ~np.array(img)  # also invert

    contours,hierarchy = findCountours(thresh)

    # For each contour, find the bounding rectangle and draw it
    # Create folder if it doesnt exist
    os.makedirs("output", exist_ok=True)
    i = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        # crop and save
        crop_img = thresh[y:y+h, x:x+w]
        if(w>=100 and h >= 100):
            # Ouput single characters files
            name = np.sum(crop_img)
            if(len(str(name)) <= 10): #remove if intensity length is > 10
                cv2.imwrite("output/"+str(i)+"-"+str(len(str(name)))+".jpg", crop_img)
            i+=1
        #Add Recty
        # if(showSample):
        #     cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
        #     cv2.putText(img, str(w)+","+str(h), (x, y), cv2.FONT_HERSHEY_SIMPLEX , 2, (0,255, 0),3 )
