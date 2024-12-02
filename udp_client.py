import socket
import threading
import random

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

def receive_messages():
    while True:
        try:
            message, _ = client.recvfrom(1024)
            message = message.decode()
            print(message)
        except:
            print("Erro ao receber mensagem.")
            break 

t1 = threading.Thread(target=receive_messages)
t1.start()

client.sendto("Novo participante no chat.".encode(), ("localhost", 12345))

while True:
    message = input()
    if message == "/sair":
        exit()
    client.sendto(message.encode(), ("localhost", 12345))
