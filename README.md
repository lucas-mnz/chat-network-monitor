# Chat and Network Monitoring System

This project implements a client-server application using TCP and UDP sockets. It includes a real-time chat system (TCP for reliability, UDP for speed) and a latency monitoring tool with UDP/ICMP. The goal is to explore networking concepts and analyze protocol differences.

## Features
- **TCP Chat System**: Reliable real-time communication with support for multiple clients.
- **UDP Chat System**: Fast, real-time communication with multiple clients, without guaranteed delivery.
- **Latency Monitoring Tool**: Tracks connection status (Normal, Slow, Inactive) using UDP/ICMP and sends notifications via email.

## Requirements
- Python 3.x
- Required Libraries: 
  - `socket`
  - `threading`
  - `time`
  - `smtplib` (for email notifications in the latency tool)

## Setup and Usage

### Chat System
1. **Run the server:**
   ```bash
   python tcp_server.py   # For TCP
   python udp_server.py   # For UDP

2. **Run the client:**
   ```bash
   python tcp_client.py   # For TCP
   python udp_client.py   # For UDP
