import numpy as np
import time
import pymongo
import cv2
import datetime
import os
import dlib
import pickle
import werkzeug
from werkzeug.utils import secure_filename
from flask import Flask, render_template, Response, redirect, url_for, request, flash
from facedetection import FaceDetectionCamera
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo import ReturnDocument
from PIL import Image
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'kimetsu no yaiba'
app.config["MONGO_URI"] = "mongodb://localhost:27017/student"
app.config["SERVER_NAME"] = 'localhost:5000'
app.config["IMAGE_UPLOADS"] = "./DataSet"
app.config["ALLOWED_IMAGE_EXTENSIONS"] = ["JPEG", "JPG", "PNG", "GIF", "WEBP"]
mongo = PyMongo(app)
app.app_context

class Controlstdata:
    def updatesj(self, oldsj_id, faculty, sj_id, sj_name, sj_StartTime, sj_FinishTime, sj_date):
        mongo.db.subject.update_one({"sj_id": oldsj_id}, {"$set": {"sj_id": sj_id, "fac_name": faculty, "sj_detail": {
            "sj_name": sj_name, "sj_StartTime": sj_StartTime+".00", "sj_FinishTime": sj_FinishTime+".00", "sj_date": sj_date}}})

    def insertnewsj(self, faculty, sj_id, sj_name, sj_StartTime, sj_FinishTime, sj_date):
        mongo.db.subject.insert(
            {"sj_id": sj_id, "fac_name": faculty, "sj_detail": {
                "sj_name": sj_name, "sj_StartTime": sj_StartTime+".00", "sj_FinishTime": sj_FinishTime+".00", "sj_date": sj_date}})

    def deletestsj(self, st_id, sj_id):
        result = mongo.db.stdata.find({'st_id': int(st_id)})
        for getresult in result:
            enrollresult = getresult['enroll']
            sjenrollresult = enrollresult['sj_enroll']
            listresult = sjenrollresult['sj_list']
            countlist = len(listresult)
            for i in range(countlist):
                txtlist = 'sj_{}'.format(i+1)
                getsj = listresult[txtlist]
                if(getsj['sj_id'] == sj_id):
                    mongo.db.stdata.find_one_and_update({"st_id": int(st_id), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): sj_id},
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

    def addSubject(self, st_id, sj_id, sj_name, sj_date, sj_begin, sj_finish):
        result = mongo.db.stdata.find({'st_id': int(st_id)})
        for getresult in result:
            enrollresult = getresult['enroll']
            sjenrollresult = enrollresult['sj_enroll']
            listresult = sjenrollresult['sj_list']
            countlist = len(listresult)
            for i in range(countlist):
                txtlist = 'sj_{}'.format(i+1)
                getsj = listresult[txtlist]
                if(getsj['sj_id'] == "-"):
                    mongo.db.stdata.find_one_and_update({"st_id": int(st_id), "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): '-'},
                                                        {"$set": {
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_id".format(i+1): sj_id,
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_name".format(i+1): sj_name,
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_date".format(i+1): sj_date,
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_begin".format(i+1): sj_begin,
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_finish".format(i+1): sj_finish,
                                                            "enroll.sj_enroll.sj_list.sj_{}.sj_chktime".format(i + 1): {"week1": {"learning_date": "-", "chk_status": "-"}, "week2": {"learning_date": "-", "chk_status": "-"}, "week3": {"learning_date": "-", "chk_status": "-"}, "week4": {"learning_date": "-", "chk_status": "-"}, "week5": {"learning_date": "-", "chk_status": "-"}, "week6": {"learning_date": "-", "chk_status": "-"}, "week7": {"learning_date": "-", "chk_status": "-"}, "week8": {"learning_date": "-", "chk_status": "-"}, "week9": {"learning_date": "-", "chk_status": "-"}, "week10": {"learning_date": "-", "chk_status": "-"}, "week11": {"learning_date": "-", "chk_status": "-"}, "week12": {"learning_date": "-", "chk_status": "-"}, "week13": {"learning_date": "-", "chk_status": "-"}, "week14": {"learning_date": "-", "chk_status": "-"}, "week15": {"learning_date": "-", "chk_status": "-"}, "week16": {"learning_date": "-", "chk_status": "-"}}}}, return_document=ReturnDocument.AFTER, upsert=True)
                    break
                else:
                    pass

    def editData(self, st_id, fname, lname, status):
        mongo.db.stdata.update_one({"st_id": int(st_id)}, {"$set": {
            "st_id": int(st_id), "f_name": fname, "l_name": lname, "st_status": status}})

    def deleteData(self, st_id):
        mongo.db.stdata.delete_one({'st_id': int(st_id)})

    def insertData(self, st_id, fname, lname, fac, br, stlevel, status):
        mongo.db.stdata.insert(
            {"st_id": int(st_id), "f_name": fname, "l_name": lname, "fac_name": fac, "br_name": br, "st_level": stlevel, "last_check": "-","st_chk": "-","st_status": status, "absent": 0,
                "late": 0,
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
                    }}}})


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
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = self.detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

@app.route('/', methods=['GET', 'POST'])
def index():
    result = mongo.db.stdata.find({})
    getfac = mongo.db.dbfaculty.find({})
    getfac2 = mongo.db.dbfaculty.find({})
    getfac3 = mongo.db.dbfaculty.find({})
    getbr = mongo.db.dbbranch.find({})
    getSubject = mongo.db.subject.find({})
    shSj = mongo.db.subject.find({})
    shSj2 = mongo.db.subject.find({})

    co1 = mongo.db.stdata.count_documents({})
    co2 = mongo.db.dbfaculty.count_documents({})
    co3 = mongo.db.subject.count_documents({})

    textpage = {"sidebartexthead": "ระบบจัดการ",
                "sidebartextbody1": "จัดการ",
                "sidebartextsubbody1": "เพิ่มนักเรียน",
                "sidebartextsubbody2": "เพิ่มวิชา",
                "sidebartextsubbody3": "เพิ่มรูปภาพ",
                "sidebartextsubbody4": "เพิ่มคณะและสาขา",
                "sidebartextbody2": "เรียนรู้",
                "sidebartextbody3": "ระบบตรวจจับ",
                "sidebartextbody4": "นับรูป", }

    return render_template('index.html', selfac=getfac3, selsj=shSj2, sendtextpage=textpage, countst=co1, countfac=co2, countsj=co3, shfaculty=getfac, shfaculty2=getfac2, shbranch=getbr, datas=result, shsj=shSj, getsj=getSubject)

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
    if request.method == "POST":
        if request.files:
            imgname = request.form['imgname']
            image = request.files["image"]
            if image.filename == "":
                flash("No image name", "warning")
                return redirect(url_for('index'))
            if allowed_image(image.filename):
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], imgname))
                flash("Upload new image {}".format(imgname), "success")
                return redirect(url_for('index'))
            else:
                flash("That file extension is not allowed", "danger")
                return redirect(url_for('index'))

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
    try:
        TD = TrainData('DataSet')
        print("\n Training faces. It will take a few seconds. Wait ...")
        faces, ids = TD.getImagesAndLabels()
        TD.recognizer.train(faces, np.array(ids))
        TD.recognizer.write('Trainer/trainer.yml')
        print("\n {0} faces trained. Exiting Program".format(
            len(np.unique(ids))))
        flash('Complete! {0} faces trained.'.format(
            len(np.unique(ids))), "success")
        return redirect(url_for('index'))
    except cv2.error:
        flash('No data for training! {0} faces trained.'.format(
            len(np.unique(ids))), "danger")
        return redirect(url_for('index'))

    # path = './DataSet/'
    # detector = dlib.get_frontal_face_detector()
    # sp = dlib.shape_predictor('./model/shape_predictor_68_face_landmarks.dat')
    # model = dlib.face_recognition_model_v1(
    #     './model/dlib_face_recognition_resnet_model_v1.dat')

    # FACE_DESC = []
    # FACE_NAME = []
    # trained = []
    # for fn in os.listdir(path):
    #     if fn.endswith('.jpg'):
    #         img = cv2.imread(path + fn)[:, :, ::-1]
    #         dets = detector(img, 1)
    #         for k, d in enumerate(dets):
    #             shape = sp(img, d)
    #             face_desc = model.compute_face_descriptor(img, shape, 5)
    #             FACE_DESC.append(np.array(face_desc))
    #             trained.append(fn)
    #             print('Training....', fn)
    #             FACE_NAME.append(fn[: fn.index('_')])

    # pickle.dump((FACE_DESC, FACE_NAME), open('./Trainer/trainset.pk', 'wb'))

    # flash('Complete! trained. {}'.format(trained), "success")
    # return redirect(url_for('index'))   


@app.route('/detection')
def detection():
    return render_template('detection.html')


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
        shSj = mongo.db.subject.find({})
        getstdata = mongo.db.stdata.find({'st_id': int(st_id)})

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

        if not st_id:
            flash('ID is empty or Not correct', "warning")
            return redirect(url_for('index'))
        if not fname:
            flash('First name is empty', "warning")
            return redirect(url_for('index'))
        if not lname:
            flash('Last name is empty', "warning")
            return redirect(url_for('index'))
        try:
            contst = Controlstdata()
            contst.insertData(st_id, fname, lname, fac, br, stlevel, status)
            flash("Welcome {0}".format(st_id), "success")
            return render_template('getdata.html', data=st_id, lvl=level)
            # return redirect(url_for('index'))
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

            flash("Add New Subject Complate {}".format(sj_id.upper()+" :: "+sj_name), "success")
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

            contst = Controlstdata()
            contst.addSubject(
                st_id, splittxt[0], splittxt[1], splittxt[4], splittxt[2], splittxt[3])

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

            contst = Controlstdata()
            contst.updatesj(oldsj_id, sj_fac, sj_id, sj_name,
                            sj_StartTime, sj_FinishTime, trandate)
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
            contst.editData(st_id, fname, lname, status)

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
    import multiprocessing as mp
    img_folder_path = './DataSet'
    dirListing = os.listdir(img_folder_path)

    n_count = len(dirListing)
    flash('Total image {0}'.format(len(dirListing)), "success")
    return redirect(url_for('index'))


@app.route("/deletestd", methods=['POST'])
def deletestd():
    if request.method == "POST":
        st_id = request.form['st_id']
        contst = Controlstdata()
        contst.deleteData(st_id)
        dirListing = os.listdir(app.config["IMAGE_UPLOADS"])
        maxlist = len(dirListing)
        # if os.path.exists("./DataSet/{0}_1.jpg".format(st_id)):
        #         os.remove(
        #             "./DataSet/{0}_1.jpg".format(st_id))
        #         print("{0}_1.jpg Deleted!".format(st_id))
        # else:
        #     pass
        for num in range(maxlist+1):
            if os.path.exists("./DataSet/{0}.{1}.{2}.jpg".format("Student", st_id, str(num))):
                os.remove(
                    "./DataSet/{0}.{1}.{2}.jpg".format("Student", st_id, str(num)))
                print("{0}.{1}.{2}.jpg Deleted!".format(
                    "Student", st_id, str(num)))
            else:
                pass
        flash('Deleted! {}'.format(st_id), "danger")
        return redirect(url_for('index'))


@app.route("/deletestsj", methods=['POST'])
def deletestsj():
    if request.method == "POST":
        stid = request.form['stid']
        sjid = request.form['sjid']

        contst = Controlstdata()
        contst.deletestsj(stid, sjid)
        flash('form {} subject {} Deleted!'.format(stid, sjid), "danger")
        return redirect(url_for('index'))


@app.route("/deletesj", methods=['POST'])
def deletesj():
    if request.method == "POST":
        sj_id = request.form['sj_id']
        mongo.db.subject.delete_one({'sj_id': sj_id})
        flash('Deleted! {}'.format(sj_id), "danger")
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
    result = mongo.db.stdata.find({'st_id': stid})
    return render_template('conclusion.html', data1=st_id, data2=sj_id, getdb=result)


@app.route('/time_feed')
def time_feed():
    def generate():
        yield datetime.now().strftime("%A %d-%m-%Y %H:%M")
    return Response(generate(), mimetype='text')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
