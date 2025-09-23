import socket
from threading import Thread

host = '10.4.1.198'
port = 5002

c_s = socket.socket()
c_s.connect((host, port))

username = input("Enter your username: ")

message = input(" > ")

def listen_for_messages():
    while True:
        data = c_s.recv(1024).decode('utf-8')
        if data:
            print(data)

t = Thread(target=listen_for_messages)
t.daemon = True
t.start()

while message.lower().strip() != 'close':
    message = f"{username}: {message}"
    c_s.send(message.encode())
    data = c_s.recv(1024).decode('utf-8')
    message = input(" > ")
c_s.close()
