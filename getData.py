import cv2
import os
import numpy as np
from PIL import Image

class generateData(object):
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    count = 0
    maxcount = 200

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.std_id = 59016400
    def __del__(self):
        self.cam.release()

    def get_frame(self):
        success, img = self.cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            self.count += 1
            showPercent = "  {0}%".format(round((self.count / self.maxcount) * 100))

            cv2.imwrite("dataset/Student." + str(self.std_id) + '.' + str(self.count) + ".jpg",
                        gray[y:y + h, x:x + w])
            cv2.putText(img, str(showPercent), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)

            if self.count >= self.maxcount:
                break

        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
