import mediapipe as mp
from playsound import playsound
import numpy as np
import cv2 as cv
import pyttsx3
import pygame
import time
import math
from numpy.lib import utils


camera = cv.VideoCapture(0)


mpPose = mp.solutions.pose
mpFaceMesh = mp.solutions.face_mesh
facemesh = mpFaceMesh.FaceMesh(max_num_faces = 2)
mpDraw = mp.solutions.drawing_utils
drawing = mpDraw.DrawingSpec(thickness = 1, circle_radius = 1,color=(0,255,0))
lineDrawingSpec = mpDraw.DrawingSpec(thickness=1, color=(0,255,0))
pose = mpPose.Pose()

lst=[]
n=0
scale = 3
ptime = 0
count = 0
brake = 0
x=250
y=300

def speak(audio):

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('rate',150)

    engine.setProperty('voice', voices[0].id)
    engine.say(audio)
    # Blocks while processing all the currently
    # queued commands
    engine.runAndWait()

def gen_frames():
    while True:
        success, img = camera.read()  # read the camera frame
        # if image feed stops
        if not success:
            break
        img_rgb = cv.cvtColor(img , cv.COLOR_BGR2RGB)
        result = pose.process(img_rgb)
        if result.pose_landmarks:
            mpDraw.draw_landmarks(img, result.pose_landmarks,mpPose.POSE_CONNECTIONS)
            for id,lm in enumerate(result.pose_landmarks.landmark):
                lst[n] = lst.append([id,lm.x,lm.y])
                n+1
                # print(lm.z)
                # if len(lst)!=0:
                #     print(lst[3])
                h , w , c = img.shape
                if id == 32 or id==31 :
                    cx1 , cy1 = int(lm.x*w) , int(lm.y*h)
                    cv.circle(img,(cx1,cy1),15,(0,0,0),cv.FILLED)
                    d = ((cx2-cx1)**2 + (cy2-cy1)**2)**0.5
                    # height = round(utils.findDis((cx1,cy1//scale,cx2,cy2//scale)/10),1)
                    di = round(d*0.5)
                    ##pygame.mixer.init()
                    ##pygame.mixer.music.load("C:\\Users\\91939\\Downloads\\New folder (2)\\New folder\\flute.mp3")
                    ##pygame.mixer.music.play()
                    dom = ((lm.z-0)**2 + (lm.y-0)**2)**0.5
                    height = round(utils.findDis((cx1,cy1//scale,cx2,cy2//scale)/10),1)
                    cv.putText(img ,"Height : ",(40,70),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),thickness=2)
                    cv.putText(img ,str(di),(180,70),cv.FONT_HERSHEY_DUPLEX,1,(0,255,0),thickness=2)
                    cv.putText(img ,"cms" ,(240,70),cv.FONT_HERSHEY_PLAIN,2,(0,0,255),thickness=2)
                    cv.putText(img ,"Stand atleast 4 meter away" ,(40,450),cv.FONT_HERSHEY_PLAIN,2,	(0,0,255),thickness=2)
                    #cv.putText(img ,"Go back" ,(240,70),cv.FONT_HERSHEY_PLAIN,2,(255,255,0),thickness=2)
                if id == 6:
                    cx2 , cy2 = int(lm.x*w) , int(lm.y*h)
                    # cx2 = cx230
                    cy2 = cy2 + 20
                    cv.circle(img,(cx2,cy2),15,(0,0,0),cv.FILLED)
        img = cv.resize(img , (2400,1200))
        ctime = time.time()
        global ptime

        fps = 1/(ctime-ptime)
        ptime=ctime
        cv.putText(img , "FPS : ",(40,30),cv.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
        cv.putText(img , str(int(fps)),(120,30),cv.FONT_HERSHEY_PLAIN,2,(0,0,0),thickness=2)
        # cv.imshow("name", img)
        # cv.waitKey(0)

        # storing data in temp file
        cv.imwrite('static/image.jpg', img)
        ret, buffer = cv.imencode('.jpg', img)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
        # concat frame one by one and show result
