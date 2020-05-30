from flask import Flask, request, redirect, url_for, flash, jsonify
import json
import os
from os import walk 
import subprocess
import sys
import shutil

def imgName():
        files = os.listdir('./img/')
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
                id = request.args.get('id')
                print('ID received:', id)
                lenID = len(id)
                nom = "./img/" + str(imgName()) + "_" + id + ".png"
                file1.save(nom)
                return "File Saved"
        elif request.method == 'GET':
                print("")

@app.route('/delete', methods=['GET'])
def bruh():
        shutil.rmtree('img')
        os.mkdir('img')
        return "Deleted img folder contents."

if __name__ == '__main__':
        p = subprocess.Popen([sys.executable, './drowsy_detection.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        #os.system('python3 ./RnD2/face_detection_eye_blink_sensor_final.py')
        app.run()
