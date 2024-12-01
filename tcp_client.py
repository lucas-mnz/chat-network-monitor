import socket
import threading
import time

last_sent_message, last_sent_message_time = "", 0

def receive_messages(client_socket):
    """Recebe mensagens do servidor"""
    global last_sent_message, last_sent_message_time
    while True:
        try:
            message = client_socket.recv(1024).decode()  # Recebe mensagens do servidor
            
            # Extrai a mensagem sem o endereço e a parte "disse: "
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
            print("Desconectado do servidor.")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 12345))  # Conecta ao servidor TCP
print("Conectado ao servidor.")

# Thread para receber mensagens do servidor
thread = threading.Thread(target=receive_messages, args=(client_socket,))
thread.start()

while True:
    message = input("Digite sua mensagem: ")
    
    # Atualiza as variáveis de controle
    last_sent_message = message
    last_sent_message_time = time.time()
    
    client_socket.send(last_sent_message.encode())  # Envia a mensagem ao servidor

    if message == "Q":
        client_socket.close()
        break
