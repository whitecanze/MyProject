import cv2 as cv

cam = cv.VideoCapture('rtsp://192.168.43.1:8080/h264_pcm.sdp')
face_detector = cv.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_default.xml')

while True:
    # ret, img = cam.read()
    # # gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # faces = face_detector.detectMultiScale(img, 1.3, 5)

    # for (x, y, w, h) in faces:
    #     cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
    #     cv.imshow('image', img)

    # k = cv.waitKey(100) & 0xff
    # if k == 27 or k == 13:  # ESC OR ENTER TO STOP
    #     break

    _, frame = cam.read()
    cv.imshow('frame', frame)
    k = cv.waitKey(100) & 0xff
    if k == 27 or k == 13:  # ESC OR ENTER TO STOP
        break
