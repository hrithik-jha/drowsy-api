import requests
import os
import cv2
import threading


def sendImage(i):
    id = 'LXklRS2NhL5aWVsvxCGn'
    image_filename = os.path.basename(i)
    multipart_form_data = {
        'image': (image_filename, open(i, 'rb')),
    }
    URL = 'http://iotproj.pythonanywhere.com/upload?id=' + id
    response = requests.post(URL, files=multipart_form_data)
        #'http://iotproj.pythonanywhere.com/upload', files=multipart_form_data)
    print(response)


def get_image():
    retval, im = camera.read()
    return im


def take_image():
    threading.Timer(10.0, take_image).start()
    for i in range(ramp_frames):
        temp = get_image()
    print("Taking image...")
    camera_capture = get_image()
    file = "./file.png"
    
    cv2.imwrite(file, camera_capture)
    sendImage("./file.png")


camera_port = 0
ramp_frames = 30
camera = cv2.VideoCapture(camera_port)
# while(True):
take_image()
# del(camera)
