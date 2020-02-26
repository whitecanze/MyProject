import numpy as np
import time
import cv2
import datetime
from datetime import timedelta
import os
import dlib
import pickle
import werkzeug
from werkzeug.utils import secure_filename
from flask import Flask, render_template, Response, redirect, url_for, request, flash, jsonify, session
import json
from bson import json_util, ObjectId
from flask_cors import CORS
from facedetection import FaceDetectionCamera
from pymongo import MongoClient
from flask_pymongo import PyMongo
from pymongo import ReturnDocument
from PIL import Image
from datetime import datetime
from passlib.hash import argon2
import pymongo

app = Flask(__name__)
app.debug = True
app.use_reloader = True
app.secret_key = 'kimetsu no yaiba'
# app.config["MONGO_URI"] = "mongodb://localhost:27017/student"
# app.config["SERVER_NAME"] = '192.168.43.116:8485'
app.config["IMAGE_UPLOADS"] = "./static/photodataset"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "WEBP"]
client = MongoClient(
    "mongodb+srv://whitecanze:benz11504@student-9fnju.gcp.mongodb.net/test?retryWrites=true&w=majority")
mongo = client.student
# mongo = PyMongo(app)
app.app_context

CORS(app, resources={r'/*': {'origins': '*'}})


class Controlstdata:
    def updatesj(self, oldsj_id, faculty, sj_id, sj_name, sj_StartTime, sj_FinishTime, sj_date, week1, week2, week3, week4, week5, week6, week7, week8, week9, week10, week11, week12, week13, week14, week15, week16):
        mongo.subject.update_one({"sj_id": oldsj_id}, {"$set": {"sj_id": sj_id, "fac_name": faculty, "sj_detail": {
            "sj_name": sj_name, "sj_StartTime": sj_StartTime+".00", "sj_FinishTime": sj_FinishTime+".00", "sj_date": sj_date, "sj_weeklist": {
                "week1": week1,
                "week2": week2,
                "week3": week3,
                "week4": week4,
                "week5": week5,
                "week6": week6,
                "week7": week7,
                "week8": week8,
                "week9": week9,
                "week10": week10,
                "week11": week11,
                "week12": week12,
                "week13": week13,
                "week14": week14,
                "week15": week15,
                "week16": week16,
            }}}})

    def insertnewsj(self, faculty, sj_id, sj_name, sj_StartTime, sj_FinishTime, sj_date):
        mongo.subject.insert(
            {"sj_id": sj_id, "fac_name": faculty, "sj_detail": {
                "sj_name": sj_name, "sj_StartTime": sj_StartTime + ".00", "sj_FinishTime": sj_FinishTime + ".00", "sj_date": sj_date, "sj_weeklist": {
                    "week1": "-",
                    "week2": "-",
                    "week3": "-",
                    "week4": "-",
                    "week5": "-",
                    "week6": "-",
                    "week7": "-",
                    "week8": "-",
                    "week9": "-",
                    "week10": "-",
                    "week11": "-",
                    "week12": "-",
                    "week13": "-",
                    "week14": "-",
                    "week15": "-",
                    "week16": "-",
                }}})

    def deletestsj(self, st_id, sj_id):
        result = mongo.stdata.find({'st_id': int(st_id)})
        for getresult in result:
            enrollresult = getresult['enroll']
            sjenrollresult = enrollresult['sj_enroll']
            listresult = sjenrollresult['sj_list']
            countlist = len(listresult)
            for i in range(countlist):
                txtlist = 'sj_{}'.format(i+1)
                getsj = listresult[txtlist]
                if(getsj['sj_id'] == sj_id):
                    mongo.stdata.find_one_and_update({"st_id": int(st_id), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): sj_id},
                                                     {"$set": {
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): "-",
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_name".format(i+1): "-",
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_date".format(i+1): "-",
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_begin".format(i+1): "-",
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_finish".format(i+1): "-",
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_chktime".format(i + 1): {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}}}, return_document=ReturnDocument.AFTER, upsert=True)
                    break
                else:
                    pass

    def addSubject(self, st_id, sj_id, sj_name, sj_date, sj_begin, sj_finish, dateweek1, dateweek2, dateweek3, dateweek4, dateweek5, dateweek6, dateweek7, dateweek8, dateweek9, dateweek10, dateweek11, dateweek12, dateweek13, dateweek14, dateweek15, dateweek16):
        result = mongo.stdata.find({'st_id': int(st_id)})
        for getresult in result:
            enrollresult = getresult['enroll']
            sjenrollresult = enrollresult['sj_enroll']
            listresult = sjenrollresult['sj_list']
            countlist = len(listresult)
            for i in range(countlist):
                txtlist = 'sj_{}'.format(i+1)
                getsj = listresult[txtlist]
                if(getsj['sj_id'] == "-"):
                    mongo.stdata.find_one_and_update({"st_id": int(st_id), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): '-'},
                                                     {"$set": {
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): sj_id,
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_name".format(i+1): sj_name,
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_date".format(i+1): sj_date,
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_begin".format(i+1): sj_begin,
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_finish".format(i+1): sj_finish,
                                                         "enroll.sj_enroll.sj_list.sj_{}.sj_chktime".format(i + 1): {"week1": {"learning_date": dateweek1, "chk_status": "-"}, "week2": {"learning_date": dateweek2, "chk_status": "-"}, "week3": {"learning_date": dateweek3, "chk_status": "-"}, "week4": {"learning_date": dateweek4, "chk_status": "-"}, "week5": {"learning_date": dateweek5, "chk_status": "-"}, "week6": {"learning_date": dateweek6, "chk_status": "-"}, "week7": {"learning_date": dateweek7, "chk_status": "-"}, "week8": {"learning_date": dateweek8, "chk_status": "-"}, "week9": {"learning_date": dateweek9, "chk_status": "-"}, "week10": {"learning_date": dateweek10, "chk_status": "-"}, "week11": {"learning_date": dateweek11, "chk_status": "-"}, "week12": {"learning_date": dateweek12, "chk_status": "-"}, "week13": {"learning_date": dateweek13, "chk_status": "-"}, "week14": {"learning_date": dateweek14, "chk_status": "-"}, "week15": {"learning_date": dateweek15, "chk_status": "-"}, "week16": {"learning_date": dateweek16, "chk_status": "-"}}}}, return_document=ReturnDocument.AFTER, upsert=True)
                    break
                else:
                    pass

    def editData(self, st_id, fname, lname, status, linetoken):
        mongo.stdata.update_one({"st_id": int(st_id)}, {"$set": {
            "st_id": int(st_id), "f_name": fname, "l_name": lname, "st_status": status, "std_line_token": linetoken}})

    def deleteData(self, st_id):
        mongo.stdata.delete_one({'st_id': int(st_id)})

    def insertData(self, st_id, fname, lname, fac, br, stlevel, status, linetoken):
        mongo.stdata.insert(
            {"st_id": int(st_id), "f_name": fname, "l_name": lname, "fac_name": fac, "br_name": br, "st_level": stlevel, "last_check": "-", "st_chk": "-", "st_status": status, "absent": 0,
                "late": 0, "std_line_token": linetoken,
             "enroll": {
                "sj_enroll": {
                    "sj_list": {
                        "sj_1": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_2": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_3": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_4": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_5": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_6": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                        "sj_7": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}},
                    }}},
             "image_list": 0
             })

    def insertImg(self, student_id, img_num):
        mongo.stdata.update_one({"st_id": int(student_id)}, {"$set": {
            "image_list": int(img_num)}})

    def deleteImg(self, student_id):
        mongo.stdata.update_one({"st_id": int(student_id)}, {"$set": {
            "image_list": 0}})

    def insertfac(self, f_id, f_name):
        mongo.dbfaculty.insert({"fac_id": f_id, "fac_name": f_name})

    def insertbr(self, b_id, b_name):
        mongo.dbbranch.insert({"br_id": b_id, "br_name": b_name})


class DataGenerator:
    font = cv2.FONT_HERSHEY_SIMPLEX
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier(
        'haarcascades/haarcascade_frontalface_default.xml')
    count = 0
    maxcount = 0

    def __init__(self, getstd_id, getlevel):
        self.cam = cv2.VideoCapture(0)
        self.std_id = getstd_id
        self.getlvl = getlevel
        if self.getlvl == "1":
            self.maxcount = 500
        elif self.getlvl == "2":
            self.maxcount = 800
        elif self.getlvl == "3":
            self.maxcount = 1000

    def __del__(self):
        self.cam.release()

    def get_frame(self):
        success, img = self.cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
        # cdt = datetime.datetime.now().strftime("%a %d-%m-%Y %H:%M:%S")
        # cv2.putText(img, cdt, (10, 20), self.font, 0.4,
        #             (255, 0, 0), 1, cv2.LINE_AA)  # TIME

        cv2.line(img, (20, 100), (20, 450), (0, 255, 0), 3)
        cv2.line(img, (20, 100), (100, 100), (0, 255, 0), 3)
        cv2.line(img, (20, 450), (100, 450), (0, 255, 0), 3)

        cv2.line(img, (620, 100), (620, 450), (0, 255, 0), 3)
        cv2.line(img, (620, 100), (540, 100), (0, 255, 0), 3)
        cv2.line(img, (620, 450), (540, 450), (0, 255, 0), 3)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            self.count += 1
            cv2.imwrite("dataset/Student." + str(self.std_id) +
                        '.' + str(self.count) + ".jpg", gray[y: y + h, x: x + w])
            cv2.putText(img, str(self.count), (x + 5, y + h - 5),
                        self.font, 1, (255, 255, 0), 1)
            # time.sleep(0.1)
        if self.count == self.maxcount:
            print("Complete!")
            self.cam.release()
        else:
            ret, jpeg = cv2.imencode('.jpg', img)
            return jpeg.tobytes()


class TrainData:
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(
        'haarcascades/haarcascade_frontalface_default.xml')

    def __init__(self, mypath):
        self.path = mypath

    def getImagesAndLabels(self):
        imagePaths = [os.path.join(self.path, f)for f in os.listdir(self.path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_cupy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_cupy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_cupy[y:y + h, x:x + w])
                ids.append(id)
        np.cuda.Stream.null.synchronize()
        return faceSamples, ids


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get("username", None) is not None:
        result = mongo.stdata.find({})
        getfac = mongo.dbfaculty.find({})
        getfac2 = mongo.dbfaculty.find({})
        getfac3 = mongo.dbfaculty.find({})
        getbr = mongo.dbbranch.find({})
        getSubject = mongo.subject.find({})
        shSj = mongo.subject.find({})
        shSj2 = mongo.subject.find({})
        imglist = mongo.dbimagelist.find({})

        co1 = mongo.stdata.count_documents({})
        co2 = mongo.dbfaculty.count_documents({})
        co3 = mongo.subject.count_documents({})
        co4 = mongo.dbimagelist.count_documents({})

        sessionname = session.get('username')

        textpage = {"sidebartexthead": "แถบเครื่องมือ",
                    "sidebartextbody1": "จัดการ",
                    "sidebartextsubbody1": "เพิ่มนักเรียน",
                    "sidebartextsubbody2": "เพิ่มวิชา",
                    "sidebartextsubbody3": "ดูรูปภาพ",
                    "sidebartextsubbody4": "เพิ่มคณะและสาขา",
                    "sidebartextbody2": "เรียนรู้",
                    "sidebartextbody3": "ระบบตรวจจับ",
                    "sidebartextbody4": "นับรูป", }

        return render_template('index.html', username=sessionname, selfac=getfac3, selsj=shSj2, sendtextpage=textpage, countst=co1, countfac=co2, countsj=co3, shfaculty=getfac, shfaculty2=getfac2, shbranch=getbr, datas=result, shsj=shSj, getsj=getSubject)
    else:
        flash('Please login!', "warning")
        return redirect(url_for('userlogin'))


def allowed_image(filename):
    if not "." in filename:
        return False
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


@app.route("/upload-image", methods=["GET", "POST"])
def upload_image():
    if session.get("username", None) is not None:
        if request.method == "POST":
            addimg = Controlstdata()
            if request.files:
                imgname = request.form['imgname']
                st_id = request.form['st_id']
                count2 = request.form['mycount']
                imgsplit = imgname.split('.')
                newname = st_id + "_" + str(int(count2) + 1) + "." + "jpg"
                image = request.files["image"]

                try:
                    print(newname)
                    if image.filename == "":
                        flash("No image file", "warning")
                        return redirect(url_for('index'))
                    if allowed_image(image.filename):
                        image.save(os.path.join(
                            app.config["IMAGE_UPLOADS"], newname))
                        addimg.insertImg(st_id, int(count2) + 1)
                        flash("Upload new image {}".format(newname), "success")
                        return redirect(url_for('index'))
                    else:
                        flash("That file extension is not allowed", "danger")
                        return redirect(url_for('index'))

                except pymongo.errors.DuplicateKeyError:
                    flash('Data is dupicate!', "danger")
                    return redirect(url_for('index'))
    else:
        flash('Please login!', "warning")
        return redirect(url_for('userlogin'))


@app.route("/addnewfac", methods=["POST"])
def addnewfac():
    if request.method == "POST":
        fac_id = request.form['fac_id']
        fac_name = request.form['fac_name']

        if not fac_id:
            flash('Please Enter Faculty ID!', "warning")
            return redirect(url_for('index'))
        if not fac_name:
            flash('Please Enter Faculty Name!', "warning")
            return redirect(url_for('index'))

        addfac = Controlstdata()
        try:
            addfac.insertfac(fac_id, fac_name)
            return redirect(url_for('index'))
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('index'))


@app.route("/addnewbr", methods=["POST"])
def addnewbr():
    if request.method == "POST":
        br_id = request.form['br_id']
        br_name = request.form['br_name']

        if not br_id:
            flash('Please Enter Branch ID!', "warning")
            return redirect(url_for('index'))
        if not br_name:
            flash('Please Enter Branch Name!', "warning")
            return redirect(url_for('index'))

        addbr = Controlstdata()
        try:
            addbr.insertbr(br_id, br_name)
            return redirect(url_for('index'))
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('index'))


@app.route("/chkimage")
def chkimage():
    return render_template('imagepage.html')


@app.route("/checkstdimg", methods=["POST"])
def chkstdimg():
    std = mongo.stdata.find({})
    response = []
    for getchk in std:
        if (getchk['image_list'] > 0):
            getchk['_id'] = str(getchk['_id'])
            response.append(getchk)
    return json.dumps(response)


@app.route("/checkstd", methods=["POST"])
def chkstd():
    std = mongo.stdata.find({})
    response = []
    for getchk in std:
        if (getchk['st_status'] == "Checked"):
            getchk['_id'] = str(getchk['_id'])
            response.append(getchk)

    return json.dumps(response)


@app.route("/stdsjchk", methods=["POST"])
def stdsjchk():
    if request.method == "POST":
        sjid = request.json['data']
        if sjid:
            std = mongo.stdata.find({})
            # print(sjid)
            response = []
            for getchk in std:
                getchk['_id'] = str(getchk['_id'])
                response.append(getchk)

            return json.dumps(response)


@app.route("/chksjlist", methods=["POST"])
def chksjlist():
    sj = mongo.subject.find({})
    response = []
    for getchk in sj:
        getchk['_id'] = str(getchk['_id'])
        response.append(getchk)

    return json.dumps(response)


@app.route('/fetchlistuser', methods=["POST"])
def fetchlistuser():
    listuser = mongo.userdata.find({})
    response = []
    for getuserlist in listuser:
        getuserlist['_id'] = str(getuserlist['_id'])
        response.append(getuserlist)

    return json.dumps(response)


@app.route('/fetchoneuser', methods=["POST"])
def fetchoneuser():
    if request.method == "POST":
        user = request.form['user']
        print(user.lower())
        listuser = mongo.userdata.find({"username": user.lower()})
        response = []
        for getuserlist in listuser:
            getuserlist['_id'] = str(getuserlist['_id'])
            response.append(getuserlist)

        return json.dumps(response)
        # return user


@app.route('/updateadmindata', methods=["POST"])
def updateadmindata():
    currentuser = request.form['currentuser']
    currentpass = request.form['currentpass']
    newpassword = request.form['newpassword']

    if not currentpass:
        return jsonify({"stat": "danger", "result": "Current Password's Empty!"})
    if not newpassword:
        return jsonify({"stat": "danger", "result": "Password's Empty!"})

    getcurrentdata = mongo.userdata.find({"username": currentuser})
    secretpass = ""
    for getc in getcurrentdata:
        secretpass = getc['password']
    chkpass = argon2.verify(currentpass, secretpass)
    print(chkpass)
    if chkpass == True:
        hashpass = argon2.using(rounds=4).hash(newpassword)
        mongo.userdata.update_one({"username": currentuser}, {
                                  "$set": {"password": hashpass}})
        getdata = mongo.userdata.find({"username": currentuser})
        result1 = ""
        result2 = ""
        result3 = ""
        for getuserlist in getdata:
            result1 = getuserlist['username']
            result2 = getuserlist['password']
            result3 = getuserlist['status']

        session.pop("username", None)
        session.clear()
        # session["username"] = result1.upper()

        return jsonify({"stat": "success", "result": "Update Success!", 'username': result1, 'password': result2, 'status': result3})
    else:
        return jsonify({"stat": "danger", "result": "Password Incorrect!"})


@app.route('/updateanotheruserdata', methods=['POST'])
def updateanotheruserdata():
    currentuser = request.form['currentuser']
    currentpass = request.form['currentpass']
    newpassword = request.form['newpassword']
    newstatus = request.form['newstatus']

    if not newpassword:
        hashpass = argon2.using(rounds=4).hash(newpassword)
        mongo.userdata.update_one({"username": currentuser}, {
                                  "$set": {"status": newstatus}})
        getdata = mongo.userdata.find({"username": currentuser})
        result1 = ""
        result2 = ""
        result3 = ""
        for getuserlist in getdata:
            result1 = getuserlist['username']
            result2 = getuserlist['password']
            result3 = getuserlist['status']

        return jsonify({"stat": "success", "result": "Update Success!", 'username': result1, 'password': result2, 'status': result3})

    if newpassword:
        hashpass = argon2.using(rounds=4).hash(newpassword)
        mongo.userdata.update_one({"username": currentuser}, {
                                  "$set": {"password": hashpass, "status": newstatus}})
        getdata = mongo.userdata.find({"username": currentuser})
        result1 = ""
        result2 = ""
        result3 = ""
        for getuserlist in getdata:
            result1 = getuserlist['username']
            result2 = getuserlist['password']
            result3 = getuserlist['status']

        return jsonify({"stat": "success", "result": "Update Success!", 'username': result1, 'password': result2, 'status': result3})


@app.route('/deleteanotheruserdata', methods=['POST'])
def deleteanotheruserdata():
    currentuser = request.form['currentuser']

    mongo.userdata.delete_one({"username": currentuser})

    return jsonify({"stat": "success", "result": "Delete Success!", "username": currentuser})


@app.route('/secure')
def securepage():
    return render_template('securepage.html')


@app.route('/gencamera')
def generate(camera):
    while True:
        # try:
        frame = camera.get_frame()
        yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        # except (RuntimeError, TypeError, NameError):
        #     print('except')


@app.route("/training")
def training():
    if session.get("username", None) is not None:
        timestart = time.time()
        path = './static/photodataset/'
        detector = dlib.get_frontal_face_detector()
        sp = dlib.shape_predictor(
            './model/shape_predictor_68_face_landmarks.dat')
        model = dlib.face_recognition_model_v1(
            './model/dlib_face_recognition_resnet_model_v1.dat')

        FACE_DESC = []
        FACE_NAME = []
        trained = []
        getcount = []
        for fn in os.listdir(path):
            if fn.endswith('.jpg'):
                img = cv2.imread(path + fn)[:, :, ::-1]
                dets = detector(img, 1)
                for k, d in enumerate(dets):
                    shape = sp(img, d)
                    face_desc = model.compute_face_descriptor(img, shape, 0)
                    FACE_DESC.append(np.array(face_desc))
                    trained.append(fn)
                    print('Training....', fn)
                    FACE_NAME.append(fn[: fn.index('_')])
        pickle.dump((FACE_DESC, FACE_NAME), open(
            './Trainer/trainset.pk', 'wb'))

        timefinish = time.time()
        totaltime = timefinish - timestart
        print("{0:.2f} s.".format(round(totaltime, 2)))
        flash('Complete! trained. {0} Time total {1:.2f} s.'.format(
            trained, totaltime), "success")
        return redirect(url_for('index'))
    else:
        flash('Please login!', "warning")
        return redirect(url_for('userlogin'))


@app.route('/userlogin')
def userlogin():
    if session.get("username", None) is not None:
        username = session.get("username", None)
        return render_template('testing.html', username=username)
    else:
        username = ""
        return render_template('testing.html', username=username)


@app.route('/adduser', methods=['POST'])
def adduser():
    if request.method == "POST":
        try:
            getuser = request.form['username']
            getpass = request.form['password']
            getkey = request.form['adminkey']
            if not getuser:
                flash('Please Enter Username!', "danger")
                return redirect(url_for('userlogin'))
            if not getpass:
                flash('Please Enter Password!', "danger")
                return redirect(url_for('userlogin'))
            if not getkey:
                if session.get("username", None) is not None:
                    hashpass = argon2.using(rounds=4).hash(getpass)
                    mongo.userdata.insert(
                        {'username': getuser.lower(), 'password': hashpass, 'status': "", "login_time": "", "logout_time": ""})
                    flash('Add user success!', "success")
                    return redirect(url_for('userlogin'))
                else:
                    flash('Please Login Or Enter Key To Create New User!', "danger")
                    return redirect(url_for('userlogin'))
            if getkey:
                user = mongo.userdata.find({})
                for chkuser in user:
                    if chkuser['status'] == "admin":
                        if chkuser['username'] == getkey:
                            hashpass = argon2.using(rounds=4).hash(getpass)
                            mongo.userdata.insert(
                                {'username': getuser, 'password': hashpass, 'status': ""})
                            flash('Add user success!', "success")
                            return redirect(url_for('userlogin'))
                        else:
                            flash('Key is incorrect!', "danger")
                            return redirect(url_for('userlogin'))
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('userlogin'))


@app.route("/chkuser",  methods=['POST'])
def chkuser():
    if request.method == "POST":
        getuser = request.form['username']
        getpass = request.form['password']
        if not getuser:
            flash('Please Enter Username!', "danger")
            return redirect(url_for('userlogin'))
        if not getpass:
            flash('Please Enter Password!', "danger")
            return redirect(url_for('userlogin'))
        gethashpass = ""
        chkpass = ""
        getuserstatus = ""
        user = mongo.userdata.find({'username': getuser})
        for chkuser in user:
            gethashpass = chkuser['password']
            chkpass = argon2.verify(getpass, gethashpass)
            getuserstatus = chkuser['status']
        if chkpass == True:
            # session.permanent = True
            # app.permanent_session_lifetime = timedelta(minutes=5)
            if getuserstatus == "admin":
                mongo.userdata.update_one({'username': getuser}, {"$set": {
                    "login_time": datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")}})
                getupdatetime = mongo.userdata.find({'username': getuser})
                login_time = ""
                for gettimec in getupdatetime:
                    login_time = gettimec['login_time']
                session["username"] = getuser.upper()
                flash(
                    f'Welcome {getuser.upper()} Login Time {login_time}', "success")
                return redirect(url_for('index'))
            else:
                flash('{} NOT HAVE PERMISSION TO ACCESS'.format(
                    getuser.upper()), "danger")
                return redirect(url_for('userlogin'))
        else:
            flash('Username Not found or Password Incorrect', "danger")
            return redirect(url_for('userlogin'))


@app.route("/userlogout")
def userlogout():
    getctime = datetime.now().strftime("%a %Y-%m-%d %H:%M:%S")
    getuser = session["username"].lower()
    mongo.userdata.update_one({'username': getuser}, {"$set": {
        "logout_time": getctime}})
    session.pop("username", None)
    session.clear()
    return redirect(url_for("userlogin"))


@app.route('/detection')
def detection():
    if session.get("username", None) is not None:
        return render_template('detection.html')
    else:
        flash('Please login!', "warning")
        return redirect(url_for('userlogin'))


@app.route('/addsj', methods=['POST'])
def addsj():
    if request.method == "POST":
        st_id = request.form['st_id']
        st_fname = request.form['st_fname']
        st_lname = request.form['st_lname']
        st_fac_name = request.form['fac_name']
        st_level = request.form['level']
        st_br_name = request.form['branch']
        datadic = {
            "st_id": st_id,
            "fname": st_fname,
            "lname": st_lname,
            "fac_name": st_fac_name,
            "br_name": st_br_name,
            "st_level": st_level,
        }
        shSj = mongo.subject.find({})
        getstdata = mongo.stdata.find({'st_id': int(st_id)})

        return render_template('addsj.html', data=datadic, sjdata=shSj, stdata=getstdata)


@app.route('/create', methods=['POST'])
def create():
    if request.method == "POST":
        st_id = request.form['st_id']
        fname = request.form['fname']
        lname = request.form['lname']
        br = request.form['branch']
        fac = request.form['faculty']
        stlevel = request.form['stlevel']
        status = request.form['st_status']
        level = request.form['level']
        linetoken = request.form['linetoken']

        if not st_id:
            flash('ID is empty or Not correct', "warning")
            return redirect(url_for('index'))
        if not fname:
            flash('First name is empty', "warning")
            return redirect(url_for('index'))
        if not lname:
            flash('Last name is empty', "warning")
            return redirect(url_for('index'))
        if not linetoken:
            linetoken = "-"
        try:
            contst = Controlstdata()
            contst.insertData(st_id, fname, lname, fac, br,
                              stlevel, status, linetoken)
            flash("Welcome {0}".format(st_id), "success")
            # return render_template('getdata.html', data=st_id, lvl=level)
            return redirect(url_for('index'))
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('index'))


@app.route('/addnewsj', methods=['POST'])
def addnewsj():
    if request.method == "POST":
        faculty = request.form['faculty']
        sj_id = request.form['sj_id']
        sj_name = request.form['sj_name']
        sj_StartTime = request.form['startime']
        sj_FinishTime = request.form['endtime']
        sj_date = request.form['day']

        if not sj_id:
            flash('Subject id is empty', "warning")
            return redirect(url_for('index'))
        if not sj_name:
            flash('Subject name is empty', "warning")
            return redirect(url_for('index'))
        if not sj_StartTime:
            flash('Start time is empty', "warning")
            return redirect(url_for('index'))
        if not sj_FinishTime:
            flash('Finish time is empty', "warning")
            return redirect(url_for('index'))
        if not sj_date:
            flash('Date is empty', "warning")
            return redirect(url_for('index'))
        try:
            trandate = None
            if sj_date == "วันจันทร์":
                trandate = "Mon"
            elif sj_date == "วันอังคาร":
                trandate = "Tue"
            elif sj_date == "วันพุธ":
                trandate = "Wed"
            elif sj_date == "วันพฤหัสบดี":
                trandate = "Thu"
            elif sj_date == "วันศุกร์":
                trandate = "Fri"
            elif sj_date == "วันเสาร์":
                trandate = "Sat"
            elif sj_date == "วันอาทิตย์":
                trandate = "Sun"

            contst = Controlstdata()
            contst.insertnewsj(faculty, sj_id.upper(), sj_name,
                               sj_StartTime, sj_FinishTime, trandate)

            flash("Add New Subject Complate {}".format(
                sj_id.upper()+" :: "+sj_name), "success")
            return redirect(url_for('index'))
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('index'))


@app.route('/addstsj', methods=['POST'])
def addstsj():
    try:
        if request.method == "POST":
            st_id = request.form['st_id']
            sj_data = request.form['sj1']
            splittxt = sj_data.split(':')

            if not sj_data:
                flash('Subject id is empty', "warning")
                return redirect(url_for('index'))
            dateweek1 = ""
            dateweek2 = ""
            dateweek3 = ""
            dateweek4 = ""
            dateweek5 = ""
            dateweek6 = ""
            dateweek7 = ""
            dateweek8 = ""
            dateweek9 = ""
            dateweek10 = ""
            dateweek11 = ""
            dateweek12 = ""
            dateweek13 = ""
            dateweek14 = ""
            dateweek15 = ""
            dateweek16 = ""
            getweeksj = mongo.subject.find({"sj_id": splittxt[0]})
            for sjd in getweeksj:
                gdetail = sjd['sj_detail']
                gweek = gdetail['sj_weeklist']
                dateweek1 = gweek['week1']
                dateweek2 = gweek['week2']
                dateweek3 = gweek['week3']
                dateweek4 = gweek['week4']
                dateweek5 = gweek['week5']
                dateweek6 = gweek['week6']
                dateweek7 = gweek['week7']
                dateweek8 = gweek['week8']
                dateweek9 = gweek['week9']
                dateweek10 = gweek['week10']
                dateweek11 = gweek['week11']
                dateweek12 = gweek['week12']
                dateweek13 = gweek['week13']
                dateweek14 = gweek['week14']
                dateweek15 = gweek['week15']
                dateweek16 = gweek['week16']

            contst = Controlstdata()
            contst.addSubject(
                st_id, splittxt[0], splittxt[1], splittxt[4], splittxt[2], splittxt[3],
                dateweek1, dateweek2, dateweek3, dateweek4, dateweek5, dateweek6, dateweek7,
                dateweek8, dateweek9, dateweek10, dateweek11, dateweek12, dateweek13, dateweek14, dateweek15, dateweek16)

            flash("Add New Subject Complate {} {}".format(
                st_id, sj_data), "success")
            return redirect(url_for('index'))

    except pymongo.errors.DuplicateKeyError:
        flash('Data is dupicate!', "danger")
        return redirect(url_for('index'))
    except werkzeug.exceptions.BadRequestKeyError:
        flash('Error! Please select subject or - ', "danger")
        return redirect(url_for('index'))


@app.route('/updatesjdata', methods=['POST'])
def updatesjdata():
    try:
        if request.method == "POST":
            sj_fac = request.form['faculty']
            oldsj_id = request.form['oldsj_id']
            sj_id = request.form['sj_id']
            sj_name = request.form['sj_name']
            sj_StartTime = request.form['startime']
            sj_FinishTime = request.form['endtime']
            sj_date = request.form['day']
            week1 = request.form['week1']
            week2 = request.form['week2']
            week3 = request.form['week3']
            week4 = request.form['week4']
            week5 = request.form['week5']
            week6 = request.form['week6']
            week7 = request.form['week7']
            week8 = request.form['week8']
            week9 = request.form['week9']
            week10 = request.form['week10']
            week11 = request.form['week11']
            week12 = request.form['week12']
            week13 = request.form['week13']
            week14 = request.form['week14']
            week15 = request.form['week15']
            week16 = request.form['week16']

            trandate = None
            if sj_date == "วันจันทร์":
                trandate = "Mon"
            elif sj_date == "วันอังคาร":
                trandate = "Tue"
            elif sj_date == "วันพุธ":
                trandate = "Wed"
            elif sj_date == "วันพฤหัสบดี":
                trandate = "Thu"
            elif sj_date == "วันศุกร์":
                trandate = "Fri"
            elif sj_date == "วันเสาร์":
                trandate = "Sat"
            elif sj_date == "วันอาทิตย์":
                trandate = "Sun"

            if not sj_id:
                flash('Subject id is empty', "warning")
                return redirect(url_for('index'))
            if not sj_name:
                flash('Subject name is empty', "warning")
                return redirect(url_for('index'))
            if not week1:
                flash('week1 is empty', "warning")
                return redirect(url_for('index'))
            if not week2:
                flash('week2 is empty', "warning")
                return redirect(url_for('index'))
            if not week3:
                flash('week3 is empty', "warning")
                return redirect(url_for('index'))
            if not week4:
                flash('week4 is empty', "warning")
                return redirect(url_for('index'))
            if not week5:
                flash('week5 is empty', "warning")
                return redirect(url_for('index'))
            if not week6:
                flash('week6 is empty', "warning")
                return redirect(url_for('index'))
            if not week7:
                flash('week7 is empty', "warning")
                return redirect(url_for('index'))
            if not week8:
                flash('week8 is empty', "warning")
                return redirect(url_for('index'))
            if not week9:
                flash('week9 is empty', "warning")
                return redirect(url_for('index'))
            if not week10:
                flash('week10 is empty', "warning")
                return redirect(url_for('index'))
            if not week11:
                flash('week11 is empty', "warning")
                return redirect(url_for('index'))
            if not week12:
                flash('week12 is empty', "warning")
                return redirect(url_for('index'))
            if not week13:
                flash('week13 is empty', "warning")
                return redirect(url_for('index'))
            if not week14:
                flash('week14 is empty', "warning")
                return redirect(url_for('index'))
            if not week15:
                flash('week15 is empty', "warning")
                return redirect(url_for('index'))
            if not week16:
                flash('week16 is empty', "warning")
                return redirect(url_for('index'))

            contst = Controlstdata()
            contst.updatesj(oldsj_id, sj_fac, sj_id, sj_name,
                            sj_StartTime, sj_FinishTime, trandate,
                            week1, week2, week3, week4, week5, week6, week7,
                            week8, week9, week10, week11, week12, week13, week14, week15, week16)
            flash("Update Subject Complate", "success")
            return redirect(url_for('index'))
    except pymongo.errors.DuplicateKeyError:
        flash('Data is dupicate!', "danger")
        return redirect(url_for('index'))
    except werkzeug.exceptions.BadRequestKeyError:
        flash('Error! Data not change ', "danger")
        return redirect(url_for('index'))


@app.route('/updatestd', methods=['POST'])
def updatestd():
    try:
        if request.method == "POST":
            st_id = request.form['st_id']
            fname = request.form['fname']
            lname = request.form['lname']
            status = request.form['st_status']
            linetoken = request.form['linetoken']

            if not st_id:
                flash('ID is empty or Not correct', "warning")
                return redirect(url_for('index'))
            if not fname:
                flash('First name is empty', "warning")
                return redirect(url_for('index'))
            if not lname:
                flash('Last name is empty', "warning")
                return redirect(url_for('index'))

            contst = Controlstdata()
            contst.editData(st_id, fname, lname, status, linetoken)

            flash("Update Student Data Complate", "success")
            return redirect(url_for('index'))
    except pymongo.errors.DuplicateKeyError:
        flash('Data is dupicate!', "danger")
        return redirect(url_for('index'))
    except werkzeug.exceptions.BadRequestKeyError:
        flash('Error! Data not change', "danger")
        return redirect(url_for('index'))


@app.route("/count")
def count():
    if session.get("username", None) is not None:
        img_folder_path1 = './DataSet'
        img_folder_path2 = './static/photodataset'
        dirListing1 = os.listdir(img_folder_path1)
        dirListing2 = os.listdir(img_folder_path2)

        n_count1 = len(dirListing1)
        n_count2 = len(dirListing2)
        flash(
            f'Total image from DataSet folder {len(dirListing1)} and Total image from photodataset folder {len(dirListing2)}', "success")
        return redirect(url_for('chkimage'))
    else:
        flash('Please login!', "warning")
        return redirect(url_for('userlogin'))


@app.route("/deletestd", methods=['POST'])
def deletestd():
    if request.method == "POST":
        st_id = request.form['st_id']
        contst = Controlstdata()
        contst.deleteData(st_id)
        dirListing1 = os.listdir(app.config["IMAGE_UPLOADS"])
        dirListing2 = os.listdir("./DataSet")
        maxlist1 = len(dirListing1)
        maxlist2 = len(dirListing2)
        for num in range(maxlist1+1):
            if os.path.exists(f"./static/photodataset/{st_id}_{str(num+1)}.jpg"):
                os.remove(
                    f"./static/photodataset/{st_id}_{str(num+1)}.jpg")
                print(f"{st_id}_1.jpg Deleted!")
            else:
                pass
        for num in range(maxlist2+1):
            if os.path.exists(f"./DataSet/Student.{st_id}.{str(num)}.jpg"):
                os.remove(
                    "./DataSet/{0}.{1}.{2}.jpg".format("Student", st_id, str(num)))
                print("{0}.{1}.{2}.jpg Deleted!".format(
                    "Student", st_id, str(num)))
            else:
                pass
        flash(f'Deleted! {st_id}', "danger")
        return redirect(url_for('index'))


@app.route("/deletestsj", methods=['POST'])
def deletestsj():
    if request.method == "POST":
        stid = request.form['stid']
        sjid = request.form['sjid']

        contst = Controlstdata()
        contst.deletestsj(stid, sjid)
        flash(f'form {stid} subject {sjid} Deleted!', "danger")
        return redirect(url_for('index'))


@app.route("/deletesj", methods=['POST'])
def deletesj():
    if request.method == "POST":
        sj_id = request.form['sj_id']
        mongo.subject.delete_one({'sj_id': sj_id})
        flash(f'Deleted! {sj_id}', "danger")
        return redirect(url_for('index'))


@app.route('/video_feed')
def video_feed():
    return Response(generate(FaceDetectionCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_getData/')
def get_data():
    myid = request.args.get('id', None)
    mylevel = request.args.get('level', None)
    print(myid)
    print(mylevel)
    return Response(generate(DataGenerator(getstd_id=myid, getlevel=mylevel)), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/stsjconclusion/<st_id>/<sj_id>', methods=['GET'])
def stsjconclusion(st_id, sj_id):
    stid = st_id
    sjid = sj_id
    result = mongo.stdata.find({'st_id': stid})
    return render_template('conclusion.html', data1=st_id, data2=sj_id, getdb=result)


@app.route('/stsjconclusionall/<st_id>', methods=['GET'])
def stsjconclusionall(st_id):
    stid = st_id
    result = mongo.stdata.find({'st_id': stid})
    return render_template('conclusionall.html', data1=st_id, getdb=result)

# @app.route('/time_feed')
# def time_feed():
#     def generate():
#         yield datetime.now().strftime("%A %d-%m-%Y %H:%M:%S")
#     return Response(generate(), mimetype='text')


if __name__ == '__main__':
    app.run(host='192.168.43.116', port='80')
