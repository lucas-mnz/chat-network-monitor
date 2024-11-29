import socket
import time

def start_udp_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(("127.0.0.1", 12345))
    print("Servidor UDP aguardando mensagens...")

    while True:
        message, addr = server_socket.recvfrom(1024)
        
        start_time = time.time()  # Marca o tempo antes de enviar a resposta
        server_socket.sendto(message, addr)  # Envia a mesma mensagem de volta
        latency = (time.time() - start_time) * 1000  # Calcula latência em ms
        print(f"Latência: {latency:.2f} ms de {addr}")

start_udp_server()
