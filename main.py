# https://stackoverflow.com/questions/33650974/opencv-python-read-specific-frame-using-videocapture
# https://stackoverflow.com/questions/24361771/frame-rate-of-video-python


import cv2
import numpy as np
      

video = cv2.VideoCapture('20231014_094039.mp4')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
count = 0

time_start = None
time_end = None

while True:
    sucess, img = video.read()
    faces = face_cascade.detectMultiScale(img, 1.3, 4)
    for(x,y,w,h) in faces:
        ROI = img[y:y+h, x:x+w]
    
        blur = cv2.GaussianBlur(ROI, (99, 99), 0)
        img[y:y+h, x:x+w] = blur
        
    
    if(type(faces).__module__ == np.__name__ and count == 0):
        time_start = (video.get(cv2.CAP_PROP_POS_MSEC))/1000
        
    if(type(faces).__module__ != np.__name__):
        time_end = (video.get(cv2.CAP_PROP_POS_MSEC))/1000
    
    #if(time_start != 0 and time_end != 0): # cut section
        

    print(f"time start: {time_start}, time end: {time_end}")
        
    
      
   
    
#   cv2.imshow("teste",img)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break

video.release()
cv2.destroyAllWindows()