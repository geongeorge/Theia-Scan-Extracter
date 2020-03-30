import glob, os
from .extract import processImage2

DATASET_FOLDER = "/dataset/"
TEMP_FOLDER = "/temporary/"

def getUrl(home,id):
    return home+DATASET_FOLDER+str(id)

def getTempUrl(home):
    return home+TEMP_FOLDER

def fileName(val): 
    return int(val.rsplit('.', 1)[0])

def listImagesIn(id,home=""): 
    #return list of images in dataset/id
    images = []
    try:
        os.chdir(home+DATASET_FOLDER+str(id))
        for file in glob.glob("*.jpg"):
            images.append(file)
        images.sort(key = fileName)
    except:
        pass
    return images
