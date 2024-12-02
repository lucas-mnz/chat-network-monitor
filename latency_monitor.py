import socket
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Definições iniciais
TARGET_IP = "127.0.0.1"  # IP do servidor
TARGET_PORT = 12345      # Porta do servidor
TIMEOUT = 2              # Em segundos
INTERVAL = 10            # Em segundos
LATENCY_NORMAL = 100
LATENCY_SLOW = 300

def send_email(status, latency):
    subject = f"Alerta de latência: {status}"
    body = f"A conexão ao {TARGET_IP}:{TARGET_PORT} está {status}.\nLatência: {latency} ms"
    
    message = MIMEMultipart()
    message["From"] = EMAIL_FROM
    message["To"] = EMAIL_TO
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.sendmail(EMAIL_FROM, EMAIL_TO, message.as_string())
        print(f"E-mail de conexão enviado: {status}")
    except Exception as e:
        print(f"Não foi possível enviar o e-mail: {e}")

def monitor_latency():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(TIMEOUT)
        while True:
            try:
                start_time = time.time()
                udp_socket.sendto(b"ping", (TARGET_IP, TARGET_PORT))
                udp_socket.recvfrom(1024)
                latency = (time.time() - start_time) * 1000  # Em milissegundos
                
                if latency < LATENCY_NORMAL:
                    print(f"Conexão Normal. Latência: {latency:.2f} ms")
                    send_email("Normal", latency)
                elif latency < LATENCY_SLOW:
                    print(f"Conexão Lenta. Latência: {latency:.2f} ms")
                    send_email("Lenta", latency)
                else:
                    print(f"Conexão Muito Lenta. Latência: {latency:.2f} ms")
                    send_email("Muito Lenta", latency)
            except socket.timeout:
                print("Conexão Inativa.")
                send_email("Inativa", "Sem Resposta")
            
            time.sleep(INTERVAL)

# Configurações do e-mail
EMAIL_TO = "nome@email.com"
SMTP_SERVER = "smtp.ethereal.email"
SMTP_PORT = 587
print("Para testes, utilize o Ethereal Mail para enviar e-mails.")
EMAIL_FROM = input("Digite o endereço de e-mail: ")
EMAIL_PASSWORD = input("Digite a senha: ")
monitor_latency()
