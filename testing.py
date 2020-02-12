# import cv2
# import numpy as np
# # import requests
from pymongo import MongoClient
from pymongo import *
# import json


client = MongoClient(
    "mongodb+srv://whitecanze:benz11504@student-9fnju.gcp.mongodb.net/test?retryWrites=true&w=majority")
db = client["student"]
getdata = db["stdata"]
result = getdata.find()

for std in result:
    print(std['st_id'])

# def testjson():
#     client = MongoClient('localhost', 27017)
#     mydb = client["student"]
#     mycol = mydb["stdata"]
#     mycol1 = mycol.find()
#     for std1 in mycol1:
#         if(std1['st_status'] == "Checked"):
#             print(std1)


# testjson()
# import cv2

# cam = cv2.VideoCapture('rtsp://192.168.43.1:8080/h264_pcm.sdp')

# while True:
#     _, frame = cam.read()
#     cv2.imshow('frame', frame)
#     cv2.waitKey(1)
