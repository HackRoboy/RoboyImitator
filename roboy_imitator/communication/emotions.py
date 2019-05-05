from roboy_imitator.common.configs import ROBOY_EMOTIONS

import socket
import struct
import logging


def receive_emotions(host, port):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.connect(server_address)
    logging.info(f"Connected to {server_address}")

    unpacker = struct.Struct("I")

    try:
        while True:
            data = sock.recv(unpacker.size)
            emotion_ind, = unpacker.unpack(data)
            yield ROBOY_EMOTIONS[list(sorted(ROBOY_EMOTIONS.keys()))[emotion_ind]]

    finally:
        sock.close()


def send_emotion(socket, emotion):
    values = list(sorted(ROBOY_EMOTIONS.values())).index(emotion)
    packer = struct.Struct('I')
    packed_data = packer.pack(values)

    try:
        socket.sendall(packed_data)
    except Exception as e:
        logging.warning(e)
