import cv2
import pickle
import numpy as np
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime
from deepface_module import analyze_face
import os

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL':  "https://computer-vision-daab1-default-rtdb.firebaseio.com/ ",
    'storageBucket': "computer-vision-daab1.appspot.com "
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
imgBackground = cv2.imread('Resources/background.png')
imgModeList = [cv2.imread(f'Resources/Modes/{img}') for img in os.listdir('Resources/Modes')]

with open('EncodeFile.p', 'rb') as file:
    encodeListKnown, studentIds = pickle.load(file)

modeType = 3
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), fx=0.25, fy=0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurrFrame = face_recognition.face_locations(imgS)
    encodeCurrFrame = face_recognition.face_encodings(imgS, faceCurrFrame)

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDis)

            if matches[matchIndex]:
                id = studentIds[matchIndex]
                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)

                if counter == 0:
                    counter = 1
                    modeType = 1

        if counter != 0:
            studentInfo = db.reference(f'Students/{id}').get()
            blob = bucket.get_blob(f"images/{id}.jpeg")
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.IMREAD_COLOR)

            last_att = datetime.strptime(studentInfo['last attendance'], "%Y-%m-%d %H:%M:%S")
            if (datetime.now() - last_att).total_seconds() > 30:
                ref = db.reference(f'Students/{id}')
                ref.child('total attendance').set(studentInfo['total attendance'] + 1)
                ref.child('last attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            if 30 < counter < 50:
                modeType = 2
            if counter <= 30:
                analysis = analyze_face(img)
                age = analysis.get('age', 'N/A')
                gender = analysis.get('gender', 'N/A')
                emotion = analysis.get('dominant_emotion', 'N/A')

                cv2.putText(imgBackground, f"{studentInfo['name']}, {age}, {gender}, {emotion}", (808, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (50, 50, 50), 1)
                imgBackground[175: 175 + 216, 909:909 + 216] = imgStudent

            counter += 1
            if counter >= 50:
                counter = 0
                modeType = 3
    else:
        modeType = 3
        counter = 0

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
