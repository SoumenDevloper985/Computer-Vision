import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials, storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://your-project-id.firebaseio.com/",
    'storageBucket': "computer-vision-daab1.appspot.com"
})

folderPath = 'images'
imgList = []
studentIds = []

for path in os.listdir(folderPath):
    img = cv2.imread(os.path.join(folderPath, path))
    if img is not None:
        imgList.append(img)
        studentIds.append(os.path.splitext(path)[0])
        blob = storage.bucket().blob(f"images/{path}")
        blob.upload_from_filename(os.path.join(folderPath, path))

def find_encodings(images):
    encode_list = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            encode_list.append(encodings[0])
    return encode_list

encodeListKnown = find_encodings(imgList)
pickle.dump([encodeListKnown, studentIds], open("EncodeFile.p", "wb"))
