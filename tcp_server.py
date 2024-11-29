import socket
import threading
import time

def handle_client(conn, addr, clients):
    print(f"Cliente conectado: {addr}")
    while True:
        try:
            start_time = time.time()  # Marca o tempo antes de receber a mensagem
            message = conn.recv(1024).decode()  # Recebe a mensagem
            latency = (time.time() - start_time) * 1000  # Calcula latência em ms
            print(f"Latência: {latency:.4f} ms de {addr}")
            
            if not message or message == "/sair":
                print(f"Cliente desconectado: {addr}")
                clients.remove(conn)
                conn.close()
                break
            print(f"{addr} disse: {message}")
            for client in clients:
                if client != conn:
                    client.send(f"{addr} disse: {message}".encode())
        except:
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", 12345))
    server_socket.listen()
    print("Servidor TCP aguardando conexões...")

    clients = []

    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.start()

start_server()
