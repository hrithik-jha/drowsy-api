import numpy as np
import cv2
import os
import requests
import json
import datetime
#import thread, winsound

face_cascade = cv2.CascadeClassifier('haarcascades\haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascades\haarcascade_eye.xml')

'''
VideoCapture with a sequence of images only works for images that are numbered consecutively starting at 0. 
It's intended as a convenience. Since your images aren't numbered like that, it's no longer a convenient to use VideoCapture. 
Simply use glob to get a list of files, sort it if necessary, and read the frames with imread in a loop.
'''
     
count = 0
iters = 0
gCount = 0

'''
ADD ARGUMENT FUNCTIONALITY FOR ID AND TIME STAMP
'''

# Add arguments for ID and Status
def sendPutRequest(idee, timestamp, isDrowsy):
  payload = {
	  "id" : idee,
    "time": timestamp,
    "isDrowsy": isDrowsy
  }
  
  #headers['content-type'] = 'application/json'

  r = requests.put("https://driver-drowsiness.herokuapp.com/addActivity", data = json.dumps(payload), headers={'Content-Type': 'application/json'})
  #requests.post(url, data=raw_data, headers={'Content-Type': 'application/x-www-form-urlencoded'})
  print(r)

while(True):
  files = os.listdir('./img')
  status = False
  if len(files) == 0:
    continue
  elif len(files) == lenOfFile:
    continue
  
  lenOfFile = len(files)
  status = False
  
  cam = cv2.VideoCapture('./img/' + files[-1])
  ret, cur = cam.read()
  # Experimental
  #r = requests.get("http://localhost:5000/test")
  gray = cv2.cvtColor(cur, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors=1, minSize=(10,10))
  for (x,y,w,h) in faces:
  	#cv2.rectangle(cur,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h,x:x+w]
    roi_color = cur[y:y+h,x:x+w]
    eyes = eye_cascade.detectMultiScale(roi_gray)
    if len(eyes) == 0:
      print ("Eyes closed")
    else:
      print ("Eyes open")
    count += len(eyes)
    iters += 1
    if iters == 2:
      iters = 0
      if count == 0:
        print ("Drowsiness Detected!")
        status = True
        #thread.start_new_thread(beep,())
      count = 0
  sendPutRequest('LXklRS2NhL5aWVsvxCGn', str(datetime.datetime.now()), status)
    #for (ex,ey,ew,eh) in eyes:
    #	cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh), (0,255,0),2)
  #cv2.imshow('frame', cur)
  # Debug sending requests

  if cv2.waitKey(1) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
    break