import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Recebe mensagens do servidor
            print(message)
        except:
            print("Desconectado do servidor.")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))
print("Conectado ao servidor.")

# Receber mensagens do servidor
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

while True:
    message = input()
    if message == "/sair":
        client_socket.close()
        exit()
    client_socket.send(message.encode())
