import speech_recognition as sr
import socket
import threading
import numpy as np
import pdb
import io
import time
from monotonic import monotonic

class MicrophoneClient:

    class AudioSource(sr.AudioSource):
        def __init__(self, id, sample_rate, chunk_size=1024):
            self.SAMPLE_WIDTH = 2
            self.SAMPLE_RATE = sample_rate
            self.CHUNK = chunk_size
            self.stream = MicrophoneClient.BytesLoop()
            self.record = False
            self.id = id
            self.name = "odas_%i"%self.id

        def __enter__(self):
            # assert self.stream is None, "This audio source is already inside a context manager"
            self.record = True
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            # self.stream = None
            self.record = False

    def __init__(self, port, host='0.0.0.0', sample_rate=16000, chunk_size=1024):
        # self.format = pyaudio.paInt16
        self.SAMPLE_WIDTH = 2#pyaudio.get_sample_size(self.format)  # size of each sample
        self.SAMPLE_RATE = sample_rate  # sampling rate in Hertz
        self.CHUNK = chunk_size
        self.CHANNELS = 1

        self.stream = MicrophoneClient.BytesLoop()

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((host, port))
        print("Micrphone client connected")

        d = threading.Thread(target=self.write_to_streams)
        self.lock = threading.RLock()
        d.setDaemon(True)
        d.start()

        self.channel = self.AudioSource(id=1, sample_rate=sample_rate, chunk_size=chunk_size)

    def write_to_streams(self):
        print("Started odas deamon")
        while True:
            data = self.s.recv(self.CHUNK)
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
