import os
import requests
from PIL import Image

SUBSCRIPTION_KEY = ""


class FaceRecognition(object):
    def __init__(self, subscription_key, image_path):
        self.subscription_key = subscription_key
        self.image_data = Image.open(image_path, "rb")
        self.face = None

    def detect_face(self):
        face_api_url = "https://westus.api.cognitive.microsoft.com/face/v1.0/detect"

        params = {
            "returnFaceId": "true",
            "returnFaceLandmarks": "true",
            "returnFaceAttributes": "age, gender, headPose, smile, facialHair, glasses, emotion"
        }

        headers = {
            "Content-Type": "application/octet/stream",
            "Ocp-Apim-Subscription-Key": self.subscription_key
        }

        response = requests.post(FACE_API_URL, params=params,
                                 headers=headers, data=self.image_data)
        response.raise_for_status()
        self.face = response.json()

    def detect_emotions():
        return self.face['emotion']

    def detect_age():
        return self.face['age']

    def detect_gender():
        return self.face['gender']


if __name__ == "__main__":
    fr = FaceRecognition()
    fr.detect_face()
    print(fr.detect_emotions())
