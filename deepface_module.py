from deepface import DeepFace

def analyze_face(image):
    try:
        result = DeepFace.analyze(img_path=image, actions=['age', 'gender', 'emotion'], enforce_detection=False)
        return result[0] if isinstance(result, list) else result
    except Exception as e:
        print("DeepFace Error:", e)
        return {}
