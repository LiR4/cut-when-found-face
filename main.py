# https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# https://stackoverflow.com/questions/24361771/frame-rate-of-video-python

import cv2
import numpy as np
import os
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from deepface import DeepFace
import os
from datetime import datetime

start_time = datetime.now()

def cut(video_file, time_start, time_end, count, second):
    ffmpeg_extract_subclip(video_file, time_start, time_end+second, targetname=f"./data/clip/cut{count}.mp4")

def filter_video(file, compare):
    video = cv2.VideoCapture(file)
    if(video.isOpened):
        while True:
            state, frames = video.read()
            if(state):
                cv2.imwrite('./teste/test.jpg', frames)
                dfs = DeepFace.find(img_path = './teste/test.jpg', db_path = compare, enforce_detection=False)
                if(len(dfs[0])!=0):
                    results.append(file)
                    break
            else:
                break
            

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
path_cut = './data/clip/'
results = []

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


for file in os.listdir(path_cut):
    print("--------\n",path_cut+file,"\n--------")
    filter_video(path_cut+file,"./teste/compare")

# filter_video("./data/clip/cut2.mp4", "./teste/compare")

print(results)

video.release()
cv2.destroyAllWindows()

end_time = datetime.now()

print('Duration: {}'.format(end_time - start_time))