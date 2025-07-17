# client/handlers.py

import socket

HOST = '127.0.0.1'
PORT = 9090

def send_request(command, username, password):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))
        message = f"{command} {username} {password}"
        print(f"[CLIENT] Sending: {message}")  # ✅ DEBUG
        client.send(message.encode())
        response = client.recv(1024).decode()
        print(f"[CLIENT] Received: {response}")  # ✅ DEBUG
        client.close()
        return response
    except Exception as e:
        print("[ERROR] Could not send request:", e)
        return "SERVER_ERROR"
