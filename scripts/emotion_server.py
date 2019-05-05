from roboy_imitator.face import mimic_emotions
from roboy_imitator.communication.emotions import send_emotion
from functools import partial
import socket
import click
import sys


@click.command()
@click.option('--host', '-h', default="0.0.0.0", help='Host')
@click.option('--port', '-p', default=10001, help='Port', type=int)
def main(host, port):
    sock = None
    try:
        while True:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = (host, port)
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind(server_address)
                sock.listen(1)
                print(f'Waiting for connections on {server_address}')
                connection, client_address = sock.accept()
                print(f'Connected to {client_address}')

                send_emotion_callback = partial(send_emotion, connection)

                # This method blocks
                mimic_emotions(send_emotion_callback)

                sock.close()

            except Exception:
                if sock:
                    sock.close()

    except KeyboardInterrupt:
        sys.exit(0)

    finally:
        if sock:
            sock.close()


if __name__ == "__main__":
    main()
