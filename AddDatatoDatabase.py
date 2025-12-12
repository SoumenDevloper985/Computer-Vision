import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://computer-vision-daab1-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "1_John": {
        "name": "John",
        "department": "CSE",
        "starting": 2023,
        "year": 2,
        "total attendance": 0,
        "last attendance": "2024-04-18 00:00:00",
        "standing": "Good"
    },
    "2_Alice": {
        "name": "Alice",
        "department": "IT",
        "starting": 2022,
        "year": 3,
        "total attendance": 0,
        "last attendance": "2024-04-18 00:00:00",
        "standing": "Excellent"
    },
    "3_Ravi": {
        "name": "Ravi",
        "department": "ECE",
        "starting": 2025,
        "year": 4,
        "total attendance": 0,
        "last attendance": "2024-04-18 00:00:00",
        "standing": "Good"
    }
}

for key, value in data.items():
    ref.child(key).set(value)