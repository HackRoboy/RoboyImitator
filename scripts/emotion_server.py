from roboy_imitator.face import mimic_emotions
from roboy_imitator.communication.emotions import send_emotion
from functools import partial
import socket
import click


@click.command()
@click.option('--host', '-h', default="0.0.0.0", help='Host')
@click.option('--port', '-p', default=10001, help='Port', type=int)
def main(host, port):
    sock = None
    connection = None
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (host, port)
        sock.bind(server_address)
        sock.listen(1)
        print(f'Waiting for connections on {server_address}')
        connection, client_address = sock.accept()
        print(f'Connected to {client_address}')

        send_emotion_callback = partial(send_emotion, connection)

        # This method blocks
        mimic_emotions(send_emotion_callback)

    finally:
        if sock:
            if connection:
                sock.shutdown(1)
            sock.close()


if __name__ == "__main__":
    main()
