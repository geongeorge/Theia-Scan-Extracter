from flask import Flask, url_for, send_from_directory, request,jsonify
import os
from werkzeug.utils import secure_filename
import uuid

app = Flask(__name__)

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