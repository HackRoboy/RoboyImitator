import os
import cv2
import requests
from PIL import Image
from io import StringIO, BytesIO
from roboy_imitator.common import CONFIGS

FACE_KEY = CONFIGS["face_key"]


class FaceRecognition(object):
    def __init__(self, face_key, image_data):
        self.face_key = face_key
        self.image_data = image_data
        self.face = None

    def detect_face(self):
        face_api_url = "https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect"

        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion',
        }

        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.face_key
        }

        response = requests.post(face_api_url, params=params,
                                 headers=headers, data=self.image_data)
        response.raise_for_status()
        self.face = response.json()

    def detect_emotions(self):
        return self.face[0]['faceAttributes']['emotion']

    def detect_age(self):
        return self.face[0]['faceAttributes']['age']

    def detect_gender(self):
        return self.face[0]['faceAttributes']['gender']


if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()

        cv2.imshow('frame', frame)
        if cv2.waitKey(33) == ord('t'):
            frame_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(frame_im)
            stream = BytesIO()
            pil_im.save(stream, format="JPEG")
            stream.seek(0)
            image_data = stream.read()
            fr = FaceRecognition(FACE_KEY, image_data)
            fr.detect_face()
            # print(fr.face)
            print(fr.detect_emotions())

        if cv2.waitKey(33) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
