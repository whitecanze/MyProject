import os
import cv2
import numpy as np
from PIL import Image


class TrainData:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(
        'haarcascades/haarcascade_frontalface_default.xml')

    def __init__(self, mypath):
        self.path = mypath

    def getImagesAndLabels(self):
        imagePaths = [os.path.join(self.path, f)
                      for f in os.listdir(self.path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids


if __name__ == '__main__':
    TD = TrainData('DataSet')
    print("\n Training faces. It will take a few seconds. Wait ...")
    faces, ids = TD.getImagesAndLabels()
    TD.recognizer.train(faces, np.array(ids))
    TD.recognizer.write('Trainer/trainer.yml')
    print("\n {0} faces trained. Exiting Program".format(len(np.unique(ids))))
