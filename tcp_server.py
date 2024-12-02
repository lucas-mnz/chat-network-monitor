import socket
import threading

clients = []  # Lista para armazenar os clients

def handle_client(conn, addr, clients):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            message = conn.recv(1024).decode() # Recebe mensagens do client
            if not message or message == "/sair":
                print(f"Cliente desconectado: {addr}")
                clients.remove(conn)
                conn.close()
                break

            print(f"{addr} disse: {message}")

            # Repassa a mensagem para os demais clients
            for client in clients:
                if client != conn:
                    client.send(f"{addr} disse: {message}".encode())

        except:
            print(f"Erro com o cliente: {addr}")
            clients.remove(conn)
            conn.close()
            break

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 12345))
server_socket.listen()
print("Servidor TCP aguardando conexões...")

while True:
    conn, addr = server_socket.accept()  # Aceita uma conexão
    clients.append(conn) 
    thread = threading.Thread(target=handle_client, args=(conn, addr, clients)) 
    thread.start() # Inicia a thread para o client

