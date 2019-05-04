import os
import cv2
import requests
import logging
from PIL import Image
from io import StringIO, BytesIO
from concurrent.futures import ThreadPoolExecutor
from roboy_imitator.common import CONFIGS

try:
    import pyroboy
    pyroboy_flag = True
except:
    pyroboy_flag = False

FACE_KEY = CONFIGS["face_key"]
ROBOY_EMOTIONS = {
    'anger': 'angry',
    'happiness': 'smile',
    'neutral': 'sweat',
    'sadness': 'speak',
    'surprise': 'blink',
    'fear': 'kiss',
    'contempt': 'blush',
    'disgust': 'blush',
}


class FaceRecognition(object):
    def __init__(self, face_key):
        self.face_key = face_key
        self.face = None
        self.executor = ThreadPoolExecutor(3)

    def detect_face(self, image_data):
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
                                 headers=headers, data=image_data)
        response.raise_for_status()
        return response.json()

    def detect_emotions(self, face):
        return face['faceAttributes']['emotion']

    def top_emotion(self, face):
        emotions = face['faceAttributes']['emotion']
        return ROBOY_EMOTIONS[max(emotions.keys(), key=lambda k: emotions[k])]

    def detect_age(self):
        return self.face[0]['faceAttributes']['age']

    def detect_gender(self):
        return self.face[0]['faceAttributes']['gender']


def main():
    fr = FaceRecognition(FACE_KEY)
    cap = cv2.VideoCapture(0)
    counter = 0

    x1, x2, y1, y2 = 0, 0, 0, 0

    def update_rectangle(frame):
        nonlocal x1
        nonlocal x2
        nonlocal y1
        nonlocal y2
        frame_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_im = Image.fromarray(frame_im)
        stream = BytesIO()
        pil_im.save(stream, format="JPEG")
        stream.seek(0)
        image_data = stream.read()
        faces = fr.detect_face(image_data)
        if len(faces) > 0:
            face = faces[0]
            x1 = int(face["faceRectangle"]["left"])
            y1 = int(face["faceRectangle"]["top"])
            x2 = x1 + int(face["faceRectangle"]["width"])
            y2 = y1 + int(face["faceRectangle"]["height"])
            logging.info(fr.detect_emotions(face))
            emotion = fr.top_emotion(face)
            logging.info('Top Emotion: ', emotion)
            try:
                if pyroboy_flag:
                    pyroboy.show_emotion(emotion)
            except Exception as e:
                logging.warning(e)
        stream.close()
        pil_im.close()

    while True:
        ret, frame = cap.read()

        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
        cv2.imshow('frame', frame)

        if counter % 46 == 0:
            fr.executor.submit(update_rectangle, frame)

        counter += 1

        if cv2.waitKey(33) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
