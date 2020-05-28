import numpy as np
import cv2
import os
import requests
import json
import datetime

face_cascade = cv2.CascadeClassifier('haarcascades\\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades\\haarcascade_eye.xml')

files = os.listdir('./img')
count = 0
iters = 0

# Sending info to main server
def sendPutRequest(idee, timestamp, isDrowsy):
    payload = {
        "id": idee,
        "time": timestamp,
        "isDrowsy": isDrowsy
    }
    #headers['content-type'] = 'application/json'

    r = requests.put("https://driver-drowsiness.herokuapp.com/addActivity",
                     data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    print(r)

lenOfFiles = len(files)

while(True):
    files = os.listdir('./img')
    status = False
    if len(files) == 0:
        continue
    #elif len(files) == lenOfFiles:
    #    continue

    print(files[1])

    lenOfFile = len(files)
    status = False

    cam = cv2.VideoCapture('./img/' + files[-1])
    ret, cur = cam.read()
    gray = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = cur[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) == 0:
            print("Eyes closed")
        else:
            print("Eyes open")
        count += len(eyes)
        iters += 1
        if iters == 2:
            iters = 0
            if count == 0:
                print("Drowsiness Detected!")
                status = True
            count = 0
    idee = files[1]
    idee = idee[::-1]
    idee = idee[4:24]
    idee = idee[::-1]
    print(idee)
    sendPutRequest(idee, str(datetime.datetime.now()), status)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break
