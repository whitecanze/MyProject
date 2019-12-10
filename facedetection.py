import cv2
import datetime
import os
from pymongo import MongoClient
from gtts import gTTS

class FaceDetectionCamera(object):
    client = MongoClient('localhost', 27017)

    db = client.student
    col = db.stdata
    col2 = db.subject
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainer/trainer.yml')
    cascadePath = "haarcascades/haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    def __init__(self):
        self.cam = cv2.VideoCapture(0)

    def __del__(self):
        self.cam.release()

    def get_frame(self):
        while True:
            success, img = self.cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            minW = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
            minH = 0.1 * self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

            cdt = datetime.datetime.now().strftime("%a %d-%m-%Y %H:%M:%S")
            txt_day = cdt.split(" ")
            txt_date = txt_day[1].split("-")
            txt_time = txt_day[2].split(":")

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.2,
                minNeighbors=5,
                minSize=(int(minW), int(minH)),
            )
            # results_subject = self.col2.find(
            #     {"sj_date": txt_day[0], "sj_StartTime": {"$gte": int(txt_time[0])}})
            # for get_subject_results in results_subject:
            #     start_time = int(get_subject_results["sj_StartTime"])
            #     finish_time = int(get_subject_results["sj_FinishTime"])
            #     sj_id = get_subject_results["sj_id"]
                # cv2.putText(img, sj_id, (540, 30), self.font, 0.8,
                #             (40, 240, 255), 2, cv2.LINE_AA)  # Subject

            # cv2.putText(img, "EXIT (ESC OR ENTER)", (10, 20), self.font, 0.4, (0, 0, 255), 1, cv2.LINE_AA)  # EXIT
            cv2.putText(img, cdt, (10, 20), self.font, 0.4,
                        (255, 0, 0), 1, cv2.LINE_AA)  # TIME

            cv2.line(img, (20, 100), (20, 450), (0, 255, 0), 3)
            cv2.line(img, (20, 100), (100, 100), (0, 255, 0), 3)
            cv2.line(img, (20, 450), (100, 450), (0, 255, 0), 3)

            cv2.line(img, (620, 100), (620, 450), (0, 255, 0), 3)
            cv2.line(img, (620, 100), (540, 100), (0, 255, 0), 3)
            cv2.line(img, (620, 450), (540, 450), (0, 255, 0), 3)

            # (20,100),(100,100)                      (620,100),(540,100)
            # _____________                                ______________
            # |                                                         |
            # |                                                         |
            # |                                                         |
            # |                                                         |
            # |(20,100),(20,450)                     (620,100),(620,450)|
            # |                                                         |
            # |                                                         |
            # |                                                         |
            # |____________                                _____________|
            # (20,450),(100,450)                      (620,450),(540,450)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # (x, y)_______
                # |           |
                # |           |
                # |           |
                # |___(x+w,y+h)

                faces_count = str(faces.shape[0])
                cv2.putText(img, "Number of faces detected: " + faces_count, (0, img.shape[0] - 10),
                            self.font, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
                id, confidence = self.recognizer.predict(gray[y: y + h, x: x + w])
                # print(id)
                if (confidence < 100):
                    results = self.col.find({"st_id": id})
                    for getresult in results:
                        getid = getresult["st_id"]
                        f_name = getresult["f_name"]
                        l_name = getresult["l_name"]
                        st_status = getresult["st_status"]
                        if (st_status == "none"):
                            query_id = {"st_id": getid}
                            set_st_status = {"$set": {"st_status": "Checked"}}
                            self.col.update_one(query_id, set_st_status)
                        else:
                            pass
                        confidence = "  {0}%".format(round(100 - confidence))
                        status = "DETECTED"
                        # cv2.putText(img, confidence, (540, 30), self.font,
                        #             0.8, (40, 240, 255), 2, cv2.LINE_AA)
                        cv2.putText(img, str(status), (170, 100),
                                    self.font, 2, (0, 255, 0), 2)
                        cv2.putText(img, str(getid), (150, 450), self.font,
                                    0.4, (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.putText(img, f_name, (230, 450), self.font,
                                    0.4, (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.putText(img, l_name, (340, 450), self.font,
                                    0.4, (255, 255, 255), 1, cv2.LINE_AA)
                        cv2.putText(img, st_status, (430, 450), self.font,
                                    0.3, (255, 255, 255,), 1, cv2.LINE_AA)
                else:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # confidence = "  {0}%".format(round(100 - confidence))
                    cv2.putText(img, "unknown", (150, 450), self.font,
                                0.4, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(img, "unknown", (230, 450), self.font,
                                0.4, (255, 255, 255), 1, cv2.LINE_AA)
                    cv2.putText(img, "unknown", (340, 450), self.font,
                                0.4, (255, 255, 255), 1, cv2.LINE_AA)

            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()
