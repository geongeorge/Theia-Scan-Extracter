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


def showImage(img):
    pilImg = processImage2(img,returnSample=True)
    pilImg.show()

def findCountours(thresh):
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    # if split, then split
    # RETR_EXTERNAL only external contours
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    return contours,hierarchy

def processImage2(img,returnSample=False, saveOutput=False):
    thresh = ~np.array(img)  # also invert
    thresh_img = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

    contours,hierarchy = findCountours(thresh)

    # For each contour, find the bounding rectangle and draw it
    # Create folder if it doesnt exist
    os.makedirs("output", exist_ok=True)
    i = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        # crop and save
        crop_img = thresh[y:y+h, x:x+w]
        if(w>=50 and h >= 50):
            if(returnSample):
                cv2.rectangle(thresh_img,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.putText(thresh_img, str(w)+","+str(h), (x, y), cv2.FONT_HERSHEY_SIMPLEX , 2, (0,255, 0),3 )
            # Ouput single characters files
            if(saveOutput):
                cv2.imwrite("output/"+str(i)+".jpg", crop_img)
            i+=1
    if(returnSample):
        pilImg = Image.fromarray(thresh_img)
        return pilImg
    else:
        return True

def saveImage(img,split=False,fl="output.jpg"):
    img.save(fl)

    if(not split):
        return

    #split so process2

    processImage2(img,returnSample=False, saveOutput=True)

