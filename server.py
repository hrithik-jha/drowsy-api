from flask import Flask, request, redirect, url_for, flash, jsonify
import json
import os
from os import walk 
import subprocess
import sys

def imgName():
        files = os.listdir('./RnD2/img/')
        return str(len(files) + 1)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/img'

@app.route('/')
def hello():
        return "Server is listening..."

@app.route('/upload', methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
                file1 = request.files['image']
                nom = "./RnD2/img/" + str(imgName()) + ".png"
                file1.save(nom)
                #detectImage(nom)
                return "File Saved"
        elif request.method == 'GET':
                print("")


if __name__ == '__main__':
        p = subprocess.Popen([sys.executable, './RnD2/face_detection_eye_blink_sensor_final.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        app.run()
