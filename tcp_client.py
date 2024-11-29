import socket
import threading
import time

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Desconectado do servidor.")
            break

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))
    print("Conectado ao servidor.")

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.start()

    while True:
        message = input()
        
        start_time = time.time()  # Marca o tempo antes de enviar a mensagem
        client_socket.send(message.encode())
        latency = (time.time() - start_time) * 1000  # Calcula latência em ms
        print(f"Latência: {latency:.4f} ms")
        
        if message == "/sair":
            client_socket.send(message.encode())
            client_socket.close()
            break

start_client()
