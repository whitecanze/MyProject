import cv2
import numpy as np
import dlib
import pickle

import datetime
import os
from pymongo import MongoClient
from gtts import gTTS


class FaceDetectionCamera(object):
    client = MongoClient('localhost', 27017)

    db = client.student
    col = db.stdata
    col2 = db.subject
    font = cv2.FONT_HERSHEY_SIMPLEX

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('Trainer/trainer.yml')
    cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)

    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        # self.cam = cv2.VideoCapture('rtsp://192.168.43.1:8080/h264_ulaw.sdp')
        self.face_detector = cv2.CascadeClassifier(
            './model/haarcascade_frontalface_default.xml')

        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(
            './model/shape_predictor_68_face_landmarks.dat')
        self.model = dlib.face_recognition_model_v1(
            './model/dlib_face_recognition_resnet_model_v1.dat')
        self.FACE_DESC, self.FACE_NAME = pickle.load(
            open('./Trainer/trainset.pk', 'rb'))

    def __del__(self):
        self.cam.release()

    def get_frame(self):

        while True:

            # ***new dlib prediction***

            _, frame = self.cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.01, 5)
            cdt = datetime.datetime.now().strftime("%a %d-%m-%Y %H:%M:%S")
            cv2.putText(frame, cdt, (10, 20), self.font, 0.4,
                        (255, 0, 0), 1, cv2.LINE_AA)  # TIME
            for (x, y, w, h) in faces:
                img = frame[y-10:y+h+10, x-10:x+w+10][:, :, ::-1]
                dets = self.detector(img, 1)
                for k, d in enumerate(dets):
                    shape = self.sp(img, d)
                    face_desc0 = self.model.compute_face_descriptor(
                        img, shape, 1)
                    d = []
                    for face_desc in self.FACE_DESC:
                        d.append(np.linalg.norm(
                            np.array(face_desc) - np.array(face_desc0)))
                    d = np.array(d)
                    idx = np.argmin(d)
                    if d[idx] < 0.5:
                        id_data = self.FACE_NAME[idx]
                        print(id_data)
                        results = self.col.find({"st_id": int(id_data)})
                        for getresult in results:
                            getid = getresult["st_id"]
                            f_name = getresult["f_name"]
                            l_name = getresult["l_name"]
                            st_status = getresult["st_status"]
                            if (st_status == "none"):
                                query_id = {"st_id": getid}
                                set_st_status = {
                                    "$set": {"last_check": cdt, "st_status": "Checked"}}
                                self.col.update_one(query_id, set_st_status)
                            else:
                                pass
                        cv2.putText(frame, id_data, (x, y-5),
                                    cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255), 2)
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    else:
                        cv2.putText(frame, "UNKNOWN", (x, y-5),
                                    cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 255), 2)
                        cv2.rectangle(
                            frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # ret, webp = cv2.imencode('.webp', frame,[cv2.IMWRITE_WEBP_QUALITY, 100])
            # return webp.tobytes()
            ret, webp = cv2.imencode('.webp', frame)
            return webp.tobytes()

            # *** Old opencv prediction ***

            # success, img = self.cam.read()
            # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # minW = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
            # minH = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

            # cdt = datetime.datetime.now().strftime("%a %d-%m-%Y %H:%M:%S")
            # txt_day = cdt.split(" ")
            # txt_date = txt_day[1].split("-")
            # txt_time = txt_day[2].split(":")

            # faces = self.faceCascade.detectMultiScale(
            #     gray,
            #     scaleFactor=1.01,
            #     minNeighbors=6,
            #     minSize=(int(minW), int(minH)),
            # )

            # # results_subject = self.col2.find(
            # #     {"sj_date": txt_day[0], "sj_StartTime": {"$gte": int(txt_time[0])}})
            # # for get_subject_results in results_subject:
            # #     start_time = int(get_subject_results["sj_StartTime"])
            # #     finish_time = int(get_subject_results["sj_FinishTime"])
            # #     sj_id = get_subject_results["sj_id"]
            # # cv2.putText(img, sj_id, (540, 30), self.font, 0.8,
            # #             (40, 240, 255), 2, cv2.LINE_AA)  # Subject

            # # cv2.putText(img, "EXIT (ESC OR ENTER)", (10, 20), self.font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)  # EXIT

            # cv2.putText(img, cdt, (10, 20), self.font, 0.4,
            #             (255, 0, 0), 1, cv2.LINE_AA)  # TIME

            # # cv2.line(img, (20, 100), (20, 450), (0, 255, 0), 3)
            # # cv2.line(img, (20, 100), (100, 100), (0, 255, 0), 3)
            # # cv2.line(img, (20, 450), (100, 450), (0, 255, 0), 3)

            # # cv2.line(img, (620, 100), (620, 450), (0, 255, 0), 3)
            # # cv2.line(img, (620, 100), (540, 100), (0, 255, 0), 3)
            # # cv2.line(img, (620, 450), (540, 450), (0, 255, 0), 3)

            # # (20,100),(100,100)                      (620,100),(540,100)
            # # _____________                                ______________
            # # |                                                         |
            # # |                                                         |
            # # |                                                         |
            # # |                                                         |
            # # |(20,100),(20,450)                     (620,100),(620,450)|
            # # |                                                         |
            # # |                                                         |
            # # |                                                         |
            # # |____________                                _____________|
            # # (20,450),(100,450)                      (620,450),(540,450)

            # for (x, y, w, h) in faces:
            #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # #     # (x, y)_______
            # #     # |           |
            # #     # |           |
            # #     # |           |
            # #     # |___(x+w,y+h)

            #     faces_count = str(faces.shape[0])
            #     cv2.putText(img, "Number of faces detected: " + faces_count, (0, img.shape[0] - 10),
            #                 self.font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            #     id, confidence = self.recognizer.predict(
            #         gray[y: y + h, x: x + w])
            #     # print(id)
            #     if (confidence < 100):
            #         results = self.col.find({"st_id": id})
            #         for getresult in results:
            #             getid = getresult["st_id"]
            #             f_name = getresult["f_name"]
            #             l_name = getresult["l_name"]
            #             st_status = getresult["st_status"]
            #             if (st_status == "none"):
            #                 query_id = {"st_id": getid}
            #                 set_st_status = {
            #                     "$set": {"last_check": cdt, "st_status": "Checked"}}
            #                 self.col.update_one(query_id, set_st_status)
            #             else:
            #                 pass
            #             confidence = "  {0}%".format(round(100 - confidence))
            #             status = "DETECTED"
            #             # cv2.putText(img, confidence, (540, 30), self.font,
            #             #             0.8, (40, 240, 255), 2, cv2.LINE_AA)
            #             cv2.putText(img, str(status), (170, 100),
            #                         self.font, 2, (0, 255, 0), 2)
            #             cv2.putText(img, str(confidence), (x+5, y+h-5),
            #                         self.font, 1, (255, 255, 0), 1)
            #             cv2.putText(img, str(getid), (150, 450), self.font,
            #                         0.4, (255, 255, 255), 1, cv2.LINE_AA)
            #             cv2.putText(img, f_name, (230, 450), self.font,
            #                         0.4, (255, 255, 255), 1, cv2.LINE_AA)
            #             cv2.putText(img, l_name, (340, 450), self.font,
            #                         0.4, (255, 255, 255), 1, cv2.LINE_AA)
            #             cv2.putText(img, st_status, (430, 450), self.font,
            #                         0.3, (255, 255, 255,), 1, cv2.LINE_AA)
            #     else:
            #         cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            #         confidence = "  {0}%".format(round(100 - confidence))
            #         cv2.putText(img, str(confidence), (x+5, y+h-5),
            #                     self.font, 1, (255, 255, 0), 1)
            #         cv2.putText(img, "unknown", (150, 450), self.font,
            #                     0.4, (255, 255, 255), 1, cv2.LINE_AA)

            # ret, jpeg = cv2.imencode('.jpg', img)
            # return jpeg.tobytes()
