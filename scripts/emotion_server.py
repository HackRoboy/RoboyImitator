from roboy_imitator.face import mimic_emotions
from roboy_imitator.communication.emotions import send_emotion
from functools import partial
import socket

host = "192.168.64.2"
port = 10001

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (host, port)
sock.connect(server_address)
print('connected to', server_address)

send_emotion_callback = partial(send_emotion, sock)

# This method blocks
mimic_emotions(send_emotion_callback)

sock.close()

