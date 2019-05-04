from roboy_imitator.common.configs import ROBOY_EMOTIONS

import socket
import struct
import logging


def receive_emotions(host="localhost", port=10000):
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (host, port)
    sock.bind(server_address)
    sock.listen(1)

    unpacker = struct.Struct("I")

    while True:
        logging.info("Waiting for a connection")
        connection, client_address = sock.accept()
        try:
            data = connection.recv(unpacker.size)
            logging.debug(f"Received {data}")
            emotion_ind, = unpacker.unpack(data)
            yield ROBOY_EMOTIONS[list(sorted(ROBOY_EMOTIONS.keys()))[emotion_ind]]

        finally:
            connection.close()


def send_emotion(socket, emotion):
    values = list(sorted(ROBOY_EMOTIONS.values())).index(emotion)
    packer = struct.Struct('I')
    packed_data = packer.pack(values)

    try:
        socket.sendall(packed_data)
    except Exception as e:
        logging.warning(e)
