from flask import Flask, url_for, send_from_directory, request,jsonify,make_response
import os
from werkzeug.utils import secure_filename
import uuid
from flask_cors import CORS

from utils.tools import listImagesIn,getUrl,getTempUrl
from utils.extract import imEncode,processImage,processImage2,getContours,saveTempFiles

app = Flask(__name__)
CORS(app)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #16 mb

def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath

@app.route('/')
def index():
    return 'Index Page'

@app.route('/images/<id>',methods=['GET'])
def listImages(id):
    images = listImagesIn(id,PROJECT_HOME)
    return jsonify(images)

#Get each image
@app.route('/show/<id>/<name>',methods=['GET'])
def showImage(id,name):
    return send_from_directory(getUrl(PROJECT_HOME,id),name)

#Get each thresholded image
@app.route('/threshold/<id>/<name>/<threshold>/<minW>/<minH>',methods=['GET'])
def showThreshImage(id,name,threshold,minW,minH):
    minW = int(minW)
    minH = int(minH)
    threshold = int(threshold)
    img = processImage(getUrl(PROJECT_HOME,id)+"/"+name,threshold)
    thresh = processImage2(img,returnSample=True, saveOutput=False,minWidth=minW,minHeight=minH)
    buffer = imEncode(thresh)
    response = make_response(buffer.tobytes())
    response.headers['Content-Type'] = 'image/jpg'
    return response


#Get each thresholded image
@app.route('/threshold/<id>/<name>/<threshold>/<minW>/<minH>/data',methods=['GET'])
def showThreshImageData(id,name,threshold,minW,minH):
    minW = int(minW)
    minH = int(minH)
    threshold = int(threshold)
    img = processImage(getUrl(PROJECT_HOME,id)+"/"+name,threshold)
    image,contours = getContours(PROJECT_HOME,img,minWidth=minW,minHeight=minH)

    response = jsonify({"image":image,"contours":contours})
    return response

#Get temporary image
@app.route('/temp/<filename>',methods=['GET'])
def tempImage(filename):
    return send_from_directory(PROJECT_HOME+"/temporary",filename)

#save from temporary to output
@app.route('/save',methods=['POST'])
def saveEverything():
    if request.method == 'GET':
        return "No direct access allowed"
    # Access data form request.form.whatever or request.data.whatever
    # { selected, selectedName, tmpImage, contours }
    # handle the tmp file
    data = request.json
    tmpImgDir = getTempUrl(PROJECT_HOME)
    saveTempFiles(home=PROJECT_HOME,selectedName=data['selectedName'],selected=data['selected'], tmpImage=data['tmpImage'], contours=data['contours'])

    return tmpImgDir
    
    # return send_from_directory(PROJECT_HOME+"/temporary",filename)

# upload image
# eg: http://127.0.0.1:5000/show/2/11.jpg

@app.route('/upload',methods=['GET', 'POST'])
def imageExtract():
    if request.method == 'GET':
        return "No direct access allowed"

    if request.method == 'POST' and request.files['image']:
        img = request.files['image']
        unique = uuid.uuid4().hex[:6]
        # Added a 6 digit uuid for duplicate images
        nameData = img.filename.rsplit('.', 1) # 0 is file name, 1 is extension
        img_name = secure_filename(nameData[0]+"-"+unique+"."+nameData[1])
        create_new_folder(app.config['UPLOAD_FOLDER'])
        saved_path = os.path.join(app.config['UPLOAD_FOLDER'], img_name)
        img.save(saved_path)
        # return url_for('uploads',filename=img_name)
        return jsonify({"name": img_name})
        # return send_from_directory(app.config['UPLOAD_FOLDER'],img_name, as_attachment=True)
    else:
        return "Where is the image?"

@app.route('/uploads/<filename>')
def uploads(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


#cv2.imencode