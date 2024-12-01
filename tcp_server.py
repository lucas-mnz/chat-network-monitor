import socket
import threading

def handle_client(conn, addr, clients):
    """Gerencia as mensagens de um cliente e as repassa para outros"""
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            message = conn.recv(1024).decode()  # Recebe a mensagem do cliente
            if not message or message == "Q":
                print(f"Cliente desconectado: {addr}")
                clients.remove(conn)  # Remove cliente desconectado
                conn.close()
                break

            print(f"{addr} disse: {message}")

            # Repassa a mensagem para os clientes
            for client in clients:
                client.send(f"{addr} disse: {message}".encode())
        except:
            print(f"Erro com o cliente: {addr}")
            clients.remove(conn)
            conn.close()
            break

def start_server():
    """Inicia o servidor TCP"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))  # Configura o IP e a porta do servidor
    server_socket.listen()
    print("Servidor TCP aguardando conexões...")

    clients = []  # Lista para armazenar conexões de clientes

    while True:
        conn, addr = server_socket.accept()  # Aceita uma conexão
        clients.append(conn)  # Adiciona o cliente à lista de conexões
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.start()

start_server()
