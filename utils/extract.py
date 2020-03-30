from PIL import Image,ImageFilter
import cv2 
import os
import uuid 
import numpy as np

# from .tools import getTempUrl,getUrl

# cannot importr manual paste

DATASET_FOLDER = "/dataset/"
TEMP_FOLDER = "/temporary/"

def getUrl(home,id):
    return home+DATASET_FOLDER+str(id)

def getTempUrl(home):
    return home+TEMP_FOLDER

# import numpy as np

def _openImage(im):
    return Image.open(im)

def saveTempFiles(home, selected, selectedName ,tmpImage,contours):
    datasetUrl = getUrl(home,selected) #dataset folder
    tempurl = getTempUrl(home) #temp folder

    #selected file and tempfile
    tmpFile = tempurl+tmpImage
    selFile = datasetUrl+"/"+selectedName

    # open temporary image
    img = cv2.imread(tmpFile,cv2.IMREAD_GRAYSCALE)

    #make output folder of not exist
    # os.makedirs("output", exist_ok=True)
    count=0
    for cnt in contours:

        crop_img = img[cnt['t']:cnt['t']+cnt['h'], cnt['l']:cnt['l']+cnt['w']]
        sub_folder = selectedName.rsplit('.')[0]
        op_folder = "output/"+str(selected)+"/"+str(sub_folder)+"/"
        os.makedirs(op_folder, exist_ok=True)
        cv2.imwrite(op_folder+str(count)+".png", crop_img)
        count+=1
    # delete temp file
    os.remove(tmpFile)
    os.rename(selFile, selFile+".done")

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

def imEncode(pil_image):
    open_cv_image = np.array(pil_image) 
    retval, buffer = cv2.imencode('.png', open_cv_image)
    return buffer

def findContours(thresh):
    thresh_color = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)
    # if split, then split
    # RETR_EXTERNAL only external contours
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    return contours,hierarchy

# get contours and temp image url
def getContours(img,minWidth=50,minHeight=50):
    thresh = ~np.array(img)  # also invert
    contours,hierarchy = findContours(thresh)
    allContours = []
    os.makedirs("temporary", exist_ok=True)
    # I think png is better
    tempName = "tmp-"+str(uuid.uuid4())+".png"
    imageUrl = "temporary/"+tempName
    cv2.imwrite(imageUrl, thresh)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        if(w>=minWidth and h >= minHeight):
            allContours.append([x,y,w,h])
    return tempName,allContours

def processImage2(img,returnSample=False, saveOutput=False,minWidth=50,minHeight=50):
    thresh = ~np.array(img)  # also invert
    thresh_img = cv2.cvtColor(thresh,cv2.COLOR_GRAY2BGR)

    contours,hierarchy = findContours(thresh)
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)

    # For each contour, find the bounding rectangle and draw it
    # Create folder if it doesnt exist
    os.makedirs("output", exist_ok=True)
    i = 0
    for cnt in contours:
        x,y,w,h = cv2.boundingRect(cnt)
        # crop and save
        crop_img = thresh[y:y+h, x:x+w]
        if(w>=minWidth and h >= minHeight):
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

