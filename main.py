# https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# https://stackoverflow.com/questions/24361771/frame-rate-of-video-python

import cv2
import numpy as np
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

def cut(video_file, time_start, time_end, count, second):
    ffmpeg_extract_subclip(video_file, time_start, time_end+second, targetname=f"./data/clip/cut{count}.mp4")

if(os.path.isdir('./data/clip') == False):
    clip = os.path.join('data', 'clip')
    os.makedirs(clip)

video_file = "data/20231014_094039.mp4"

video = cv2.VideoCapture(video_file)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

count = 0
last_time = []
time_start = 0.0
time_end = 0.0
seconds = 3

while True:
    sucess, img = video.read()
    faces = face_cascade.detectMultiScale(img, 1.3, 4)
        
    if(type(faces).__module__ == np.__name__):
        time_start = (video.get(cv2.CAP_PROP_POS_MSEC))/1000
        last_time.append(time_start)
        
    if(type(faces).__module__ != np.__name__):
        time_end = (video.get(cv2.CAP_PROP_POS_MSEC))/1000
    
    if(time_start != 0.0 and time_end != 0.0): # cut section
        if(last_time[count]+1 < time_start):
            cut(video_file, time_start, time_end, count, seconds)
            print(f"time start: {time_start}, time end: {time_end+seconds}")
            count += 1

        time_start = 0.0
        time_end = 0.0
    
    # cv2.imshow("teste",img)
    if sucess != True:
        break

video.release()
cv2.destroyAllWindows()