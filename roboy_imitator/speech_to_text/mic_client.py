import speech_recognition as sr
import socket
import threading
import numpy as np
import pdb
import io
import time
from monotonic import monotonic


class MicrophoneClient:

    def __init__(self, port, host='0.0.0.0', sample_rate=16000, chunk_size=1024):
        # self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = 2#pyaudio.get_sample_size(self.format)  # size of each sample
        self.SAMPLE_RATE = sample_rate  # sampling rate in Hertz
        self.CHUNK = chunk_size
        self.CHANNELS = 1
        self.record = False

        self.stream = MicrophoneClient.BytesLoop()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print("Microphone client connected")

        d = threading.Thread(target=self.write_to_streams)
        self.lock = threading.RLock()
        d.setDaemon(True)
        d.start()

    def write_to_streams(self):
        print("Started mic client deamon")
        while True:
            data = self.s.recv(self.CHUNK)
            if self.record:
                data = np.frombuffer(data, dtype=np.int16)
                self.stream.write(data.tobytes())

    def __enter__(self):
        # assert self.stream is None, "This audio source is already inside a context manager"
        self.record = True
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # self.stream = None
        self.record = False

    class BytesLoop:
        def __init__(self, s=b''):
            self.buffer = s
            self.lock = threading.RLock()

        def read(self, n=-1):
            # print("read %i"%n)
            while len(self.buffer) < n:
               
                pass
            #print("got enough data")
            # self.lock.acquire()

            chunk = self.buffer[:n]
            self.buffer = self.buffer[n:]
            # self.lock.release()
            return chunk

        def write(self, s):
            # print("write %i"%len(s))
            # self.lock.acquire()
            self.buffer += s
            # self.lock.release()
