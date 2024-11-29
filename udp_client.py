import socket
import threading
import time

def receive_messages(client_socket):
    while True:
        try:
            message, addr = client_socket.recvfrom(1024)
            print(f"Mensagem recebida de {addr}: {message.decode()}")
        except:
            print("Erro ao receber mensagem.")
            break

def start_udp_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ("127.0.0.1", 12345)

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        
        start_time = time.time()  # Marca o tempo antes de enviar a mensagem
        client_socket.sendto(message.encode(), server_address)
        latency = (time.time() - start_time) * 1000  # Calcula latência em ms
        print(f"Latência: {latency:.2f} ms")
        
        if message == "/sair":
            break

    client_socket.close()

start_udp_client()
