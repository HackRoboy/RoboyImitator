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
            emotion = unpacker.unpack(data)
            yield emotion

        finally:
            connection.close()
