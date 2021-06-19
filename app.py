import os, glob
from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
# from src.test import main
# from srrescgan.predict import main_srrescgan
import numpy as np
import time
import subprocess

UPLOAD_FOLDER = 'static/uploads/'
DOWNLOAD_FOLDER = 'static/downloads/'
ALLOWED_EXTENSIONS = {'jpg', 'png', '.jpeg'}
app = Flask(__name__, static_url_path="/static")

# APP CONFIGURATIONS
app.config['SECRET_KEY'] = 'opencv'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 6mb
app.config['MAX_CONTENT_LENGTH'] = 6 * 1024 * 1024
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        model = request.form.get('comp_select')
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            # ul = glob.glob('./static/downloads/*')
            # for f in ul:
            #     os.remove(f)
            ul = glob.glob('./static/uploads/*')
            for f in ul:
                os.remove(f)
            filename = secure_filename(file.filename)
            filename = filename.split('.')[0] + '_{}_'.format(model.lower()) + '.jpg'
            with open('./data/test.txt', 'w+') as f:
                f.write('./static/downloads/{}'.format(filename))
            f.close()
            file.save(os.path.join(DOWNLOAD_FOLDER, filename))
            process_file(os.path.join(DOWNLOAD_FOLDER, filename), filename, model)

            data = {
                "original_img": 'static/downloads/{}'.format(filename),
                "processed_img": 'static/uploads/{}'.format(filename.split('.')[0]+'.png')
            }
            return render_template("index.html", data=data)
    return render_template('index.html')


def process_file(path, filename, model):
    # print(model.upper())
    if model.upper() == 'RESNET50':
        subprocess.call("python infer_val.py --dataset 'pascal_voc' --mask-output-dir './results' --infer-list './data/test.txt' --exp 'baselines' --run 'v1' --resume 'e012Xs0.902' --cfg './configs/voc_resnet50.yaml'",shell=True)
    else:
        subprocess.call("python infer_val.py --dataset 'pascal_voc' --mask-output-dir './results' --infer-list './data/test.txt' --exp 'resnet38' --run 'v1' --resume 'e020Xs0.928' --cfg './configs/voc_resnet38.yaml'",shell=True)
    # elif model == 'SRResCGAN':
    #     main_srrescgan()


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True, port=80)
