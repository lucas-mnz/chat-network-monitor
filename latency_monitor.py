import socket
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configurações do monitoramento
TARGET_IP = "127.0.0.1"  # IP do destino para monitorar
TARGET_PORT = 12345      # Porta do destino
TIMEOUT = 2              # Tempo limite para resposta (em segundos)
INTERVAL = 10            # Intervalo entre os pings (em segundos)

# Escala de latência (em milissegundos)
LATENCY_NORMAL = 100
LATENCY_SLOW = 300

# Configurações do e-mail - utilize Ethereal para testes
EMAIL_FROM = "email@ethereal.email"
EMAIL_PASSWORD = "senha temporária"
EMAIL_TO = "nome@email.com"
SMTP_SERVER = "smtp.ethereal.email"
SMTP_PORT = 587

def send_email(status, latency):
    """Envia um e-mail com o status da conexão."""
    subject = f"Latency Alert: {status}"
    body = f"The connection to {TARGET_IP}:{TARGET_PORT} is {status}.\nLatency: {latency} ms"
    
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
        print(f"Alert email sent: {status}")
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor_latency():
    """Monitora a latência da conexão usando UDP."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.settimeout(TIMEOUT)
        while True:
            try:
                start_time = time.time()
                udp_socket.sendto(b"ping", (TARGET_IP, TARGET_PORT))
                udp_socket.recvfrom(1024)
                latency = (time.time() - start_time) * 1000  # Em milissegundos
                
                if latency < LATENCY_NORMAL:
                    print(f"Connection Normal. Latency: {latency:.2f} ms")
                    send_email("Normal", latency)
                elif latency < LATENCY_SLOW:
                    print(f"Connection Slow. Latency: {latency:.2f} ms")
                    send_email("Slow", latency)
                else:
                    print(f"Connection Very Slow. Latency: {latency:.2f} ms")
                    send_email("Very Slow", latency)
            except socket.timeout:
                print("Connection Inactive.")
                send_email("Inactive", "No response")
            
            time.sleep(INTERVAL)

monitor_latency()
