import threading as t
import socket

HOST = "10.4.1.198"
#HOST = "127.0.0.1"
PORT = 5002
listeConn = []

def handle_connection(connexion, address):
    with connexion:
        print(f"Connecté en tant que {address}")
        listeConn.append(connexion)
        while True:
            data = connexion.recv(1024)
            if not data:
                break
            message = data.decode('utf-8')  
            print(message)
            for conn in listeConn:
                 conn.sendall(message.encode('utf-8'))      
            


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    while True:
        s.listen()
        conn, addr = s.accept()
        client_thread = t.Thread(target=handle_connection, args=(conn, addr))
        client_thread.start()

