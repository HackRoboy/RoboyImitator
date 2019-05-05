#/usr/bin/python3
import rclpy
from roboy_cognition_msgs.msg import RecognizedSpeech
from roboy_cognition_msgs.srv import RecognizeSpeech
import speech_recognition as sr
import threading
from roboy_imitator.speech_to_text.recognizer import *
from roboy_imitator.speech_to_text.mic_client import MicrophoneClient
import click
from time import sleep


def callback(request, response):
    global bing, src
    try:
        text = bing.recognize(src)
        response.text = text
        print("text: " + text)
    except sr.UnknownValueError:
        print("Microsoft Bing Voice Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Microsoft Bing Voice Recognition service; {0}".format(e,))

    return response


def listener(source, node):
    global bing, src, publisher
    publisher = node.create_publisher(RecognizedSpeech, '/roboy/cognition/speech/recognition')
    src = source
    bing = SpeechToText()

    with bing:
        srv = node.create_service(RecognizeSpeech, '/roboy/cognition/speech/recognition', callback)

        # with source as source:
        while rclpy.ok():
            #sleep(1)
            rclpy.spin_once(node)

        #node.destroy_service(srv)
        #node.destroy_publisher(publisher)
        #rclpy.shutdown()


def odas_recognition(node):
    from ros2_speech_recognition.odas_sr_driver import Odas
    print("waiting for odas connection")
    o = Odas(port=10002, chunk_size=2048)

    listeners = []
    for i in range(4):
        listeners.append(threading.Thread(target=listener, args = (o.channels[i], node, )))
    for l in listeners:
        l.start()


def odas_single_channel(node):
    from ros2_speech_recognition.odas_sr_driver import Odas
    print("waiting for odas connection")
    o = Odas(host="192.168.64.1", port=10002, chunk_size=4096)
    listener(o.channels[0], node)


def mic_recognition(node):
    mic = sr.Microphone()
    listener(mic, node)


def client_recognition(node, host, port):
    mic_client = MicrophoneClient(host=host, port=port, chunk_size=4096)
    listener(mic_client, node)


@click.command()
@click.option('--mic_host', default="192.168.0.215", help='Microphone host which sends recording chunks')
@click.option('--mic_port', default=10002, help='Microphone port', type=int)
def main(mic_host, mic_port):
    rclpy.init()
    node = rclpy.create_node('odas_speech_recognition')
    client_recognition(node, mic_host, mic_port) # requires RPi running odas
    # mic_recognition(node)
    # odas_recognition(node)


if __name__ == '__main__':
    main()
