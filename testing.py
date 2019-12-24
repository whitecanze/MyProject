import cv2
import numpy as np
import dlib

cap = cv2.VideoCapture(0)

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("./model/shape_predictor_68_face_landmarks.dat")

while True:
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = detector(gray)
    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2 = face.bottom()
        #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

        landmarks = predictor(gray, face)

        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            cv2.circle(frame, (x, y), 4, (255, 0, 0), -1)

    cv2.imshow("Frame", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break

# import requests
# from pymongo import MongoClient
# from pymongo import *
# client = MongoClient('localhost', 27017)

# db = client.student
# col = db.testarray
# stdata = db.stdata
# stsj = db.stsubject
# sj = db.subject


# def getTestArray():
#     # result = col.find({'st_id': "2"})
#     # for getresult in result:
#     #     getenroll = getresult['enroll']
#     #     getlist = getenroll['sj_enroll']
#     #     getd = getlist['sj_list']
#     #     getsjid = getd['sj_id']
#     #     getsjname = getd['sj_name']
#     #     print(getsjid)
#     #     print(getsjname)
#         # getd = getresult['sj_1']
#         # print(getd['sj_timetable'])
#     getstdata = stdata.find({'st_id': 59016400})
#     for shstdata in getstdata:
#         # print(shstdata['enroll'])
#         getenroll = shstdata['enroll']
#         getstenroll = getenroll['sj_enroll']
#         getlist = getstenroll['sj_list']
#         print(len(getlist))
#     # getsj = sj.find({})

#     # for getsjdata in getsj:
#     #     getsjid = getsjdata['sj_id']
#     #     getsjdetail = getsjdata['sj_detail']
#     #     print(getsjdata['sj_detail'].document_count())
#     #     getlist = getsjid + ":" + getsjdetail['sj_name']
#     #     getsplit = getlist.split(':')
#     #     print(getsplit[0], getsplit[1])


# def updateTestArray():
#     myquery = {"st_id": "2"}
#     newvalues = {"$set": {"enroll": {
#         "sj_enroll": {"sj_list": {"sj_id": "1", "sj_name": "Hello World"}}}}}
#     col.update_one(myquery, newvalues)


# def testline(txtmsg):
#     #!/usr/local/bin/python
#     # -*- coding: utf-8 -*-

#     url = 'https://notify-api.line.me/api/notify'
#     token = 'aZuYld5Iy6svashgzG7Q2dlxJpDjP6fpxOL11Nhyn57'
#     headers = {'content-type': 'application/x-www-form-urlencoded','Authorization': 'Bearer '+token}

#     msg = txtmsg
#     r = requests.post(url, headers=headers, data={'message': msg})
#     print(r.text)


# if __name__ == '__main__':
#     # getTestArray()
#     # updateTestArray()
#     txtmsg = "ทดสอบ"
#     testline(txtmsg)
