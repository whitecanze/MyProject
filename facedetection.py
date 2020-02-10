import cv2
import numpy as np
import cupy as cp
import dlib
import pickle
import requests
import datetime
import os
from pymongo import MongoClient
from gtts import gTTS
import time


class FaceDetectionCamera(object):
    client = MongoClient('localhost', 27017)

    db = client.student
    stddatadb = db.stdata
    subjectdatadb = db.subject
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
            timestart = time.time()

            # ***new dlib prediction***

            _, frame = self.cam.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray, 1.2, 5)
            cdt = datetime.datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
            splitdate = cdt.split(" ")
            chkday = splitdate[0]
            chkdate = splitdate[1]
            chktime = splitdate[2]
            splitcurrenttime = chktime.split(":")
            currenthour = splitcurrenttime[0]
            currentminute = splitcurrenttime[1]
            currentsecond = splitcurrenttime[2]
            getchkday = ""

            if chkday == "Sun":
                getchkday = "วันอาทิตย์"
            elif chkday == "Mon":
                getchkday = "วันจันทร์"
            elif chkday == "Tue":
                getchkday = "วันอังคาร"
            elif chkday == "Wed":
                getchkday = "วันพุธ"
            elif chkday == "Thu":
                getchkday = "วันพฤหัสบดี"
            elif chkday == "Fri":
                getchkday = "วันศุกร์"
            elif chkday == "Sat":
                getchkday = "วันเสาร์"

            findsj = self.subjectdatadb.find({"sj_detail.sj_date": chkday})
            findcomparesj = self.subjectdatadb.find({"sj_detail.sj_date": chkday})
            
            getcompare = 0
            getsjid = ""
            getsjname = ""
            getsjweek = ""
            getsjstatus = ""
            countdatasj = 0
            testgettime = []
            testgettime2 = []
            testgetsjid = []
            testgetsjname = []

            for compare1 in findcomparesj:
                if compare1['sj_id']:
                    getcompare += 1
            # print("getcompare:"+str(getcompare))
            if(getcompare>1):
                for getfindsj in findsj:
                    getdetail = getfindsj['sj_detail']
                    getweek = getdetail['sj_weeklist']
                    getdetailstart = getdetail['sj_StartTime']
                    getdetailfinish = getdetail['sj_FinishTime']
                    getsplitstarttime = getdetailstart.split(".")
                    getsplitfinishtime = getdetailfinish.split(".")

                    testgettime.append(getdetail['sj_StartTime'].split(".")[0])
                    testgettime2.append(getdetail['sj_FinishTime'].split(".")[0])
                    testgetsjid.append(getfindsj['sj_id'])
                    testgetsjname.append(getdetail['sj_name'])
                    # print(testgettime)
                    # print(testgettime2)
                    # print(testgetsjid)
                    # print(testgetsjname)
                    if len(testgettime) > 1:
                        # print("1:"+str(int(currenthour)-int(testgettime[0])))
                        # print("2:"+str(int(currenthour)-int(testgettime[1])))
                        print("more than 1 subject")
                        if (int(currenthour) - int(testgettime[0])) < (int(currenthour) - int(testgettime[1])):
                            print("subject 1 case")
                            if int(currenthour) < int(testgettime[0]) or (int(currenthour) >= int(testgettime[0]) and int(currenthour) <= int(testgettime2[0])):
                                print("มาเรียน")
                                getsjid = testgetsjid[0]
                                getsjname = testgetsjname[0]
                                if int(currenthour) >= int(testgettime[0]) and int(currentminute) > 15:
                                    getsjstatus = "late"
                                    print(getsjstatus)
                                elif int(currenthour) == int(testgettime[0]) and int(currentminute) <= 15:
                                    getsjstatus = "duly"
                                    print(getsjstatus)
                                elif int(currenthour) < int(testgettime[0]):
                                    getsjstatus = "duly"
                                    print(getsjstatus)
                                findsj2 = self.subjectdatadb.find({"sj_id": getsjid})
                                for getfindsj2 in findsj2:
                                    getfinddetail = getfindsj2['sj_detail']
                                    getfindweek = getfinddetail['sj_weeklist']
                                    for myweek in range(16):
                                        if getfindweek['week{0}'.format(myweek + 1)] == chkdate:
                                            getsjweek = "week{0}".format(myweek + 1)

                            elif int(currenthour) >= int(testgettime2[0]):
                                print("ไม่มาเรียน")
                                getsjstatus = "absent"
                                getall = self.stddatadb.find({})
                                getsjid = testgetsjid[0]
                                getsjname = testgetsjname[0]
                                getsjweek2 = ""

                                findsj2 = self.subjectdatadb.find({"sj_id": getsjid})
                                for getfindsj2 in findsj2:
                                    getfinddetail = getfindsj2['sj_detail']
                                    getfindweek = getfinddetail['sj_weeklist']
                                    for myweek in range(16):
                                        if getfindweek['week{0}'.format(myweek + 1)] == chkdate:
                                            getsjweek2 = "week{0}".format(myweek + 1)

                                for chkall in getall:
                                    getid = chkall["st_id"]
                                    f_name = chkall["f_name"]
                                    l_name = chkall["l_name"]
                                    stdabsent = chkall["absent"]
                                    gettoken = chkall["std_line_token"]
                                    st_status = chkall["st_status"]
                                    enrollresult = chkall['enroll']
                                    sjenrollresult = enrollresult['sj_enroll']
                                    listresult = sjenrollresult['sj_list']
                                    countlist = len(listresult)

                                    if chkall['st_status'] == "none":
                                        for dbi in range(countlist):
                                            txtlist = 'sj_{}'.format(dbi+1)
                                            getsj = listresult[txtlist]
                                            getlistweek = getsj['sj_chktime']
                                            getthisweek = getlistweek[getsjweek2]
                                            if getsj['sj_id'] == getsjid:
                                                if getthisweek['chk_status'] == "-":
                                                    query_all = {"st_id": int(getid), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(dbi+1): getsjid}
                                                    setall_std_sj_status = {"$set": {"absent":int(stdabsent)+1,"enroll.sj_enroll.sj_list.sj_{0}.sj_chktime.{1}.chk_status".format(dbi + 1, getsjweek2): getsjstatus}}
                                                    self.stddatadb.update_one(query_all, setall_std_sj_status)
                                                else:
                                                    pass
                                    elif chkall["st_status"] == "Checked":
                                        query_idafter = {"st_id": getid}
                                        set_st_statusafter = {
                                            "$set": {"st_status": "none"}}
                                        self.stddatadb.update_one(
                                            query_idafter, set_st_statusafter)
                            else:
                                print("ไม่เข้าเงื่อนไข")
                        else:
                            print("subject 2 case")
                            if int(currenthour) < int(testgettime[1]) or (int(currenthour) >= int(testgettime[1]) and int(currenthour) <= int(testgettime2[1])):
                                print("มาเรียน")
                                getsjid = testgetsjid[1]
                                getsjname = testgetsjname[1]
                                if int(currenthour) >= int(testgettime[1]) and int(currentminute) > 15:
                                    getsjstatus = "late"
                                    print(getsjstatus)
                                elif int(currenthour) == int(testgettime[1]) and int(currentminute) <= 15:
                                    getsjstatus = "duly"
                                    print(getsjstatus)
                                elif int(currenthour) < int(testgettime[1]):
                                    getsjstatus = "duly"
                                    print(getsjstatus)
                                findsj2 = self.subjectdatadb.find({"sj_id": getsjid})
                                for getfindsj2 in findsj2:
                                    getfinddetail = getfindsj2['sj_detail']
                                    getfindweek = getfinddetail['sj_weeklist']
                                    for myweek in range(16):
                                        if getfindweek['week{0}'.format(myweek + 1)] == chkdate:
                                            getsjweek = "week{0}".format(myweek + 1)

                            elif int(currenthour) >= int(testgettime2[1]):
                                print("ไม่มาเรียน")
                                getsjstatus = "absent"
                                getall = self.stddatadb.find({})
                                getsjid = testgetsjid[1]
                                getsjname = testgetsjname[1]
                                getsjweek2 = ""

                                findsj2 = self.subjectdatadb.find({"sj_id": getsjid})
                                for getfindsj2 in findsj2:
                                    getfinddetail = getfindsj2['sj_detail']
                                    getfindweek = getfinddetail['sj_weeklist']
                                    for myweek in range(16):
                                        if getfindweek['week{0}'.format(myweek + 1)] == chkdate:
                                            getsjweek2 = "week{0}".format(myweek + 1)

                                for chkall in getall:
                                    getid = chkall["st_id"]
                                    f_name = chkall["f_name"]
                                    l_name = chkall["l_name"]
                                    stdabsent = chkall["absent"]
                                    gettoken = chkall["std_line_token"]
                                    st_status = chkall["st_status"]
                                    enrollresult = chkall['enroll']
                                    sjenrollresult = enrollresult['sj_enroll']
                                    listresult = sjenrollresult['sj_list']
                                    countlist = len(listresult)

                                    if chkall['st_status'] == "none":
                                        for dbi in range(countlist):
                                            txtlist = 'sj_{}'.format(dbi+1)
                                            getsj = listresult[txtlist]
                                            getlistweek = getsj['sj_chktime']
                                            getthisweek = getlistweek[getsjweek2]
                                            if getsj['sj_id'] == getsjid:
                                                if getthisweek['chk_status'] == "-":
                                                    query_all = {"st_id": int(getid), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(dbi+1): getsjid}
                                                    setall_std_sj_status = {"$set": {"absent":int(stdabsent)+1,"enroll.sj_enroll.sj_list.sj_{0}.sj_chktime.{1}.chk_status".format(dbi + 1, getsjweek2): getsjstatus}}
                                                    self.stddatadb.update_one(query_all, setall_std_sj_status)
                                                else:
                                                    pass
                                    elif chkall["st_status"] == "Checked":
                                        query_idafter = {"st_id": getid}
                                        set_st_statusafter = {"$set": {"st_status": "none"}}
                                        self.stddatadb.update_one(query_idafter, set_st_statusafter)
                            else:
                                print("ไม่เข้าเงื่อนไข")
            elif getcompare == 1:
                print("just 1 subject")
                for getfindsj in findsj:
                    getdetail = getfindsj['sj_detail']
                    getweek = getdetail['sj_weeklist']
                    getdetailstart = getdetail['sj_StartTime']
                    getdetailfinish = getdetail['sj_FinishTime']
                    getsplitstarttime = getdetailstart.split(".")
                    getsplitfinishtime = getdetailfinish.split(".")

                    if int(currenthour) < int(getsplitstarttime[0]) or (int(currenthour) >= int(getsplitstarttime[0]) and int(currenthour) <= int(getsplitfinishtime[0])):
                        getsjid = getfindsj['sj_id']
                        getsjname = getdetail['sj_name']
                        if int(currenthour) >= int(getsplitstarttime[0]) and int(currentminute) > 15:
                            getsjstatus = "late"
                        elif int(currenthour) == int(getsplitstarttime[0]) and int(currentminute) <= 15:
                            getsjstatus = "duly"
                        elif int(currenthour) < int(getsplitstarttime[0]):
                            getsjstatus = "duly"
                        for myweek in range(16):
                            if getweek['week{0}'.format(myweek + 1)] == chkdate:
                                getsjweek = "week{0}".format(myweek + 1)

                    elif int(currenthour) >= int(getsplitfinishtime[0]):
                        getsjstatus = "absent"
                        getall = self.stddatadb.find({})
                        getsjid = getfindsj['sj_id']
                        getsjname = getdetail['sj_name']
                        getsjweek2 = ""

                        for myweek in range(16):
                            if getweek['week{0}'.format(myweek + 1)] == chkdate:
                                getsjweek2 = "week{0}".format(myweek + 1)

                        for chkall in getall:
                            getid = chkall["st_id"]
                            f_name = chkall["f_name"]
                            l_name = chkall["l_name"]
                            stdabsent = chkall["absent"]
                            gettoken = chkall["std_line_token"]
                            st_status = chkall["st_status"]
                            enrollresult = chkall['enroll']
                            sjenrollresult = enrollresult['sj_enroll']
                            listresult = sjenrollresult['sj_list']
                            countlist = len(listresult)

                            if chkall['st_status'] == "none":
                                for dbi in range(countlist):
                                    txtlist = 'sj_{}'.format(dbi+1)
                                    getsj = listresult[txtlist]
                                    getlistweek = getsj['sj_chktime']
                                    getthisweek = getlistweek[getsjweek2]
                                    if getsj['sj_id'] == getsjid:
                                        if getthisweek['chk_status'] == "-":
                                            query_all = {"st_id": int(getid), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(dbi+1): getsjid}
                                            setall_std_sj_status = {"$set": {"absent": int(stdabsent)+1, "enroll.sj_enroll.sj_list.sj_{0}.sj_chktime.{1}.chk_status".format(dbi + 1, getsjweek2): getsjstatus}}
                                            self.stddatadb.update_one(query_all, setall_std_sj_status)
                                        else:
                                            pass
                            elif chkall["st_status"] == "Checked":
                                query_idafter = {"st_id": getid}
                                set_st_statusafter = {"$set": {"st_status": "none"}}
                                self.stddatadb.update_one(query_idafter, set_st_statusafter)
            # TIME
            # cv2.putText(frame, cdt, (10, 20), self.font, 0.4,(255, 0, 0), 1, cv2.LINE_AA)  
            for (x, y, w, h) in faces:
                img = frame[y-10:y+h+10, x-10:x+w+10][:, :, ::-1]
                dets = self.detector(img)
                for k, d in enumerate(dets):
                    shape = self.sp(img, d)
                    face_desc0 = self.model.compute_face_descriptor(
                        img, shape)
                    d = []
                    for face_desc in self.FACE_DESC:
                        d.append(np.linalg.norm(np.array(face_desc) - np.array(face_desc0)))
                    d = np.array(d)
                    idx = np.argmin(d)
                    if d[idx] < 0.5:
                        id_data = self.FACE_NAME[idx]
                        print(id_data)
                        results = self.stddatadb.find({"st_id": int(id_data)})
                        for getresult in results:
                            getid = getresult["st_id"]
                            f_name = getresult["f_name"]
                            l_name = getresult["l_name"]
                            stdlate = getresult["late"]
                            gettoken = getresult["std_line_token"]
                            st_status = getresult["st_status"]
                            enrollresult = getresult['enroll']
                            sjenrollresult = enrollresult['sj_enroll']
                            listresult = sjenrollresult['sj_list']
                            countlist = len(listresult)

                            if st_status == "none":
                                if (getsjweek):
                                    sendstatus = ""
                                    newstdlate = 0
                                    if getsjstatus == "duly":
                                        sendstatus = "ตรงเวลา"
                                    elif getsjstatus == "late":
                                        sendstatus = "สาย"
                                        newstdlate = int(stdlate)+1

                                    # update st_status
                                    query_id = {"st_id": getid}
                                    set_st_status = {
                                        "$set": {"last_check": cdt, "st_status": "Checked", "late": newstdlate}}
                                    self.stddatadb.update_one(
                                        query_id, set_st_status)

                                    # update st subject
                                    for dbi in range(countlist):
                                        txtlist = 'sj_{}'.format(dbi+1)
                                        getsj = listresult[txtlist]
                                        if getsj['sj_id'] == getsjid:
                                            query_at = {"st_id": int(
                                                getid), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(dbi+1): getsjid}
                                            set_std_sj_status = {"$set": {
                                                "enroll.sj_enroll.sj_list.sj_{0}.sj_chktime.{1}.chk_status".format(dbi + 1, getsjweek): getsjstatus}}
                                            self.stddatadb.update_one(
                                                query_at, set_std_sj_status)
                                    # line notify
                                    if(gettoken):
                                        url = 'https://notify-api.line.me/api/notify'
                                        token = gettoken
                                        headers = {
                                            'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer '+token}
                                        msg = 'วิชา {0}:{1} รหัสนิสิต {2} ชื่อ {3} {4} เช็คชื่อแล้ว ณ {5} ที่ {6} เวลา {7} สถานะ {8}'.format(getsjid,getsjname,
                                            getid, f_name, l_name, getchkday, chkdate, chktime, sendstatus,getsjstatus)
                                        r = requests.post(
                                            url, headers=headers, data={'message': msg})
                                    else:
                                        pass
                                else:
                                    pass

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
            timefinish = time.time()
            totaltime = timefinish - timestart
            ffps = self.cam.get(cv2.CAP_PROP_FPS)
            fps = (ffps/totaltime)/ffps
            print("{0:.2f} s.".format(round(totaltime, 2)))
            print("FPS:{0:.2f} ".format(round(fps, 2)))
            cv2.putText(frame, "FPS:{0:.2f} ".format(round(fps, 2)), (10, 20), self.font,
                        0.4, (0, 255, 0), 1, cv2.LINE_AA)
            ret, jpeg = cv2.imencode('.jpg', frame,[int(cv2.IMWRITE_JPEG_QUALITY), 100])
            return jpeg.tobytes()

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
