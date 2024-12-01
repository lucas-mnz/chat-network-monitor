import socket
import threading
import queue
import time

message_queue = queue.Queue()
clients = set()

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("localhost", 12345))
print("Servidor UDP aguardando mensagens...")

def receive():
    while True:
        try:
           message, addr = server_socket.recvfrom(1024)
           message_queue.put((message, addr))
           print(f"Mensagem recebida de {addr}")
        except:
            print("Erro ao receber mensagem.")

def broadcast():
    while True:
        while not message_queue.empty():
            message, addr = message_queue.get()
            print(message.decode())
            if addr not in clients:
                clients.add(addr)
            for client in clients:
                try:
                    server_socket.sendto(f"{addr} disse: {message.decode()}".encode(), client)
                    print(f"Enviando mensagem para {client}")
                except:
                    clients.remove(client)

t1 = threading.Thread(target=receive)
t2 = threading.Thread(target=broadcast)

t1.start()
t2.start()
