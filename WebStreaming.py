from flask import Flask, render_template, Response, redirect, url_for, request, flash
from facedetection import FaceDetectionCamera
from flask_pymongo import PyMongo
from pymongo import MongoClient
from pymongo import ReturnDocument
import pymongo
import cv2
import datetime
import os
import numpy as np
import time
from PIL import Image
import werkzeug

app = Flask(__name__)
app.secret_key = 'kimetsu no yaiba'
app.config["MONGO_URI"] = "mongodb://localhost:27017/student"
app.config["SERVER_NAME"] = 'localhost:5000'
mongo = PyMongo(app)
app.app_context


class Controlstdata:
    
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
                                "enroll.sj_enroll.sj_list.sj_{}.sj_chktime".format(i + 1): {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-", "week16": "-"}}}
                        , return_document=ReturnDocument.AFTER, upsert=True)
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
                {"st_id": int(st_id), "f_name": fname, "l_name": lname, "fac_name": fac, "br_name": br, "st_level": stlevel, "st_status": status, "absent": 0,
                    "late": 0,
                "enroll": {
                    "sj_enroll": {
                        "sj_list": {
                            "sj_1": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_2": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_3": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_4": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_5": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_6": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-","week16": "-"}},
                            "sj_7": {"sj_id": "-", "sj_name": "-", "sj_date": "-", "sj_begin": "-", "sj_finish": "-", "sj_chktime": {"week1": "-", "week2": "-", "week3": "-", "week4": "-", "week5": "-", "week6": "-", "week7": "-", "week8": "-", "week9": "-", "week10": "-", "week11": "-", "week12": "-", "week13": "-", "week14": "-", "week15": "-", "week16": "-"}}
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
        cdt = datetime.datetime.now().strftime("%a %d-%m-%Y %H:%M:%S")
        cv2.putText(img, cdt, (10, 20), self.font, 0.4,
                    (255, 0, 0), 1, cv2.LINE_AA)  # TIME

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
    getbr = mongo.db.dbbranch.find({})
    getSubject = mongo.db.subject.find({})
    shSj = mongo.db.subject.find({})
    return render_template('index.html', shfaculty=getfac, shbranch=getbr, datas=result, shsj=shSj, getsj=getSubject)


@app.route('/gencamera')
def generate(camera):
    while True:
        try:
            frame = camera.get_frame()
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        except (RuntimeError, TypeError, NameError):
            print('except')


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
        getstdata = mongo.db.stdata.find({'st_id':int(st_id)})

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
        except pymongo.errors.DuplicateKeyError:
            flash('Data is dupicate!', "danger")
            return redirect(url_for('index'))


@app.route('/newsj', methods=['POST'])
def addnewsj():
    if request.method == "POST":
        sj_id = request.form['sj_id']
        sj_name = request.form['sj_name']
        sj_StartTime = request.form['sj_stt']
        sj_FinishTime = request.form['sj_fnt']
        sj_date = request.form['sj_d']

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
            mongo.db.subject.insert(
                {"sj_id": sj_id, "sj_name": sj_name, "sj_StartTime": sj_StartTime, "sj_FinishTime": sj_FinishTime, "sj_date": sj_date})
            flash("Add New Subject Complate", "success")
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
            contst.addSubject(st_id, splittxt[0], splittxt[1], splittxt[4], splittxt[2], splittxt[3])
            
            flash("Add New Subject Complate {} {}".format(
                st_id, sj_data), "success")
            return redirect(url_for('index'))

    except pymongo.errors.DuplicateKeyError:
        flash('Data is dupicate!', "danger")
        return redirect(url_for('index'))
    except werkzeug.exceptions.BadRequestKeyError:
        flash('Error! Please select subject or - ', "danger")
        return redirect(url_for('index'))


@app.route('/updatesj', methods=['POST'])
def updatesj():
    try:
        if request.method == "POST":
            sj_id = request.form['sj_id']
            sj_name = request.form['sj_name']
            sj_StartTime = request.form['sj_stt']
            sj_FinishTime = request.form['sj_fnt']
            sj_date = request.form['sj_d']

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
        mongo.db.subject.update_one({"sj_id": sj_id}, {"$set": {
                                    "sj_id": sj_id, "sj_name": sj_name, "sj_StartTime": sj_StartTime, "sj_FinishTime": sj_FinishTime, "sj_date": sj_date}})
        flash("Update Subject Complate", "success")
        return redirect(url_for('index'))
    except pymongo.errors.DuplicateKeyError:
        flash('Data is dupicate!', "danger")
        return redirect(url_for('index'))
    except werkzeug.exceptions.BadRequestKeyError:
        flash('Error! Please select day ', "danger")
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
        flash('Error! Please select none or checked ', "danger")
        return redirect(url_for('index'))


@app.route("/count")
def count():
    import multiprocessing as mp
    img_folder_path = 'G:/Project/DataSet'
    dirListing = os.listdir(img_folder_path)

    n_count = len(dirListing)
    flash('Total image {0}'.format(len(dirListing)), "success")
    return redirect(url_for('index'))


@app.route("/delete/<st_id>", methods=['GET'])
def delete(st_id):
    contst = Controlstdata()
    contst.deleteData(st_id)
    img_folder_path = 'G:/project/DataSet/'
    dirListing = os.listdir(img_folder_path)
    maxlist = len(dirListing)
    for num in range(maxlist+1):
        if os.path.exists("G:/project/DataSet/{0}.{1}.{2}.jpg".format("Student", st_id, str(num))):
            os.remove(
                "G:/project/DataSet/{0}.{1}.{2}.jpg".format("Student", st_id, str(num)))
            print("{0}.{1}.{2}.jpg Deleted!".format(
                "Student", st_id, str(num)))
        else:
            pass
    flash('Deleted!', "danger")
    return redirect(url_for('index'))


@app.route("/deletesj/<sj_id>", methods=['GET'])
def deletesj(sj_id):
    mongo.db.subject.delete_one({'sj_id': sj_id})
    flash('Deleted!', "danger")
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
