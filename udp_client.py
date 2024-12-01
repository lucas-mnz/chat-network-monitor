import socket
import threading
import random
import time

last_sent_message, last_sent_message_time = "", 0

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client.bind(("localhost", random.randint(8000, 9000)))

def receive_messages():
    global last_sent_message, last_sent_message_time
    while True:
        try:
            message, _ = client.recvfrom(1024)
            message = message.decode()
            if " disse: " in message:
                received_message = message.split(" disse: ")[1]
            else:
                received_message = message
            if received_message == last_sent_message:
                latency = (time.time() - last_sent_message_time) * 1000
                print(f"Latência: {latency:} ms")
            else:
                print(message)
        except:
            print("Erro ao receber mensagem.")
            break 

t1 = threading.Thread(target=receive_messages)
t1.start()

client.sendto("Novo participante no chat.".encode(), ("localhost", 12345))

while True:
    message = input()
    if message == "Q":
        exit()
    last_sent_message = message
    last_sent_message_time = time.time()
    client.sendto(message.encode(), ("localhost", 12345))
