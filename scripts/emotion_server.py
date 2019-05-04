#!/usr/bin/env python
import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind(('localhost', 10003))
serversocket.listen(1)
print("Emotion Server Started")

conn, addr = serversocket.accept()
print('Connected by', addr)

while True:

    try:
        emotion = conn.recv(1024)

        if not emotion:
            break

        print("Emotion: ", emotion)
        
    except socket.error:
        print("Error Occured.")
        break

conn.close()
serversocket.close()