from pymongo import MongoClient
from pymongo import * 
client = MongoClient('localhost', 27017)

db = client.student
col = db.testarray
stdata = db.stdata
stsj = db.stsubject
sj = db.subject


def getTestArray():
    # result = col.find({'st_id': "2"})
    # for getresult in result:
    #     getenroll = getresult['enroll']
    #     getlist = getenroll['sj_enroll']
    #     getd = getlist['sj_list']
    #     getsjid = getd['sj_id']
    #     getsjname = getd['sj_name']
    #     print(getsjid)
    #     print(getsjname)
        # getd = getresult['sj_1']
        # print(getd['sj_timetable'])
    getstdata = stdata.find({'st_id': 59016400})
    for shstdata in getstdata:
        # print(shstdata['enroll'])
        getenroll = shstdata['enroll']
        getstenroll = getenroll['sj_enroll']
        getlist = getstenroll['sj_list']
        print(len(getlist))
    # getsj = sj.find({})
    
    # for getsjdata in getsj:
    #     getsjid = getsjdata['sj_id']
    #     getsjdetail = getsjdata['sj_detail']
    #     print(getsjdata['sj_detail'].document_count())
    #     getlist = getsjid + ":" + getsjdetail['sj_name']
    #     getsplit = getlist.split(':')
    #     print(getsplit[0], getsplit[1])


def updateTestArray():
    myquery = {"st_id": "2"}
    newvalues = {"$set": {"enroll": {
        "sj_enroll": {"sj_list": {"sj_id": "1", "sj_name": "Hello World"}}}}}
    col.update_one(myquery, newvalues)


if __name__ == '__main__':
    getTestArray()
    # updateTestArray()


# result = stdata.find()
# for getr in result:
#     getd = getr
#     print(getr)

# result = stsj.find()
# for getsj in result:
#     get1 = getsj['sj_1']
#     gets = get1['sj_id']
#     print(gets)

# def getdt(mydt):
#     g1 = mydt[0]
#     g2 = mydt[1]
#     g3 = mydt.split['.']
#     print(g1)
#     print(g2)
#     print(g3)


# outp = {1.1,2.1,3.1}
# getdt(outp)

# std_id = "59016400"
# name = "Phatcharapong Jullamonton"
# sj1 = "ER0413"
# sjn1 = "กฏหมายและจริยธรรมทางคอมพิวเตอร์"
# sjstr1 = "9"
# sjfin1 = "12"
# sjdate1 = "Wed"
# sj2 = "ER0415"
# sjn2 = "โครงงานวิศวกรรมคอมพิวเตอร์ 2"
# sjstr2 = "13"
# sjfin2 = "16"
# sjdate2 = "Wed"
# sj3 = "ER0423"
# sjn3 = "เทคโนโลยีธุรกิจอิเล็กทรอนิกส์"
# sjstr3 = "9"
# sjfin3 = "13"
# sjdate3 = "Tue"
# sj4 = "ER0433"
# sjn4 = "การบริหารจัดการระบบเครือข่าย"
# sjstr4 = "12"
# sjfin4 = "16"
# sjdate4 = "Mon"
# sj5 = ""
# sjn5 = ""
# sjstr5 = ""
# sjfin5 = ""
# sjdate5 = ""
# sj6 = ""
# sjn6 = ""
# sjstr6 = ""
# sjfin6 = ""
# sjdate6 = ""
# sj7 = ""
# sjn7 = ""
# sjstr7 = ""
# sjfin7 = ""
# sjdate7 = ""

# col.insert_one({"st_id": std_id, "st_name": name,
#                 "sj_enroll": {
#                     "sj_1": {
#                         "sj_id": sj1,
#                         "sj_name": sjn1,
#                         "sj_StartTime": sjstr1,
#                         "sj_FinishTime": sjfin1,
#                         "sj_date": sjdate1
#                     },
#                     "sj_2": {
#                         "sj_id": sj2,
#                         "sj_name": sjn2,
#                         "sj_StartTime": sjstr2,
#                         "sj_FinishTime": sjfin2,
#                         "sj_date": sjdate2
#                     },
#                     "sj_3": {
#                         "sj_id": sj3,
#                         "sj_name": sjn3,
#                         "sj_StartTime": sjstr3,
#                         "sj_FinishTime": sjfin3,
#                         "sj_date": sjdate3
#                     },
#                     "sj_4": {
#                         "sj_id": sj4,
#                         "sj_name": sjn4,
#                         "sj_StartTime": sjstr4,
#                         "sj_FinishTime": sjfin4,
#                         "sj_date": sjdate4
#                     },
#                     "sj_5": {
#                         "sj_id": sj5,
#                         "sj_name": sjn5,
#                         "sj_StartTime": sjstr5,
#                         "sj_FinishTime": sjfin5,
#                         "sj_date": sjdate5
#                     },
#                     "sj_6": {
#                         "sj_id": sj6,
#                         "sj_name": sjn6,
#                         "sj_StartTime": sjstr6,
#                         "sj_FinishTime": sjfin6,
#                         "sj_date": sjdate6
#                     },
#                     "sj_7": {
#                         "sj_id": sj7,
#                         "sj_name": sjn7,
#                         "sj_StartTime": sjstr7,
#                         "sj_FinishTime": sjfin7,
#                         "sj_date": sjdate7
#                     }
#                 }})
