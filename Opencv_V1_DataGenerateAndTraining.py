import cv2
from pymongo import MongoClient
import os
import numpy as np
from PIL import Image


class GenerateData:
    client = MongoClient('localhost', 27017)
    db = client.student
    col = db.stdata

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("Error: Could not open camera.")
        exit()
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_default.xml')
    count = 0
    maxcount = 200

    def __init__(self, std_id, f_name, l_name, st_status, mypath):
        self.std_id = std_id
        self.f_name = f_name
        self.l_name = l_name
        self.st_status = st_status
        self.path = mypath

    # Insert
    def insertData(self):
        self.col.insert_one({"st_id": self.std_id, "f_name": self.f_name, "l_name": self.l_name, "st_status": self.st_status})
        print("\n Initializing face capture. Look the camera and wait ...")

    def startGetData(self):
        while True:
            ret, img = self.cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                self.count += 1
                showPercent = "  {0}%".format(round((self.count / self.maxcount) * 100))

                cv2.imwrite("dataset/Student." + str(self.std_id) + '.' + str(self.count) + ".jpg",
                            gray[y:y + h, x:x + w])
                cv2.putText(img, str(showPercent), (x + 5, y + h - 5), self.font, 1, (255, 255, 0), 1)
                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff
            if k == 27 or k == 13:  # ESC OR ENTER TO STOP
                break
            elif self.count >= self.maxcount:
                break

    def getImagesAndLabels(self):
        imagePaths = [os.path.join(self.path, f) for f in os.listdir(self.path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.face_detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids


if __name__ == '__main__':
    DTP = 'DataSet'
    st_status = 'none'
    student_id = int(input('enter student id ==>  '))
    first_name = input('enter first name ==>  ')
    last_name = input('enter last name  ==>  ')
    gDT = GenerateData(student_id,first_name,last_name,st_status,DTP)
    gDT.insertData()
    gDT.startGetData()
    print("\n Training faces. It will take a few seconds. Wait ...")
    faces, ids = gDT.getImagesAndLabels()
    gDT.recognizer.train(faces, np.array(ids))
    gDT.recognizer.write('Trainer/trainer.yml')
    print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))
    print("\n Exiting Program and cleanup stuff")
    gDT.cam.release()
    cv2.destroyAllWindows()
