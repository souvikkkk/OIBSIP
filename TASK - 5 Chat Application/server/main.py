import socket
import threading
from auth import handle_register, handle_login
from database import init_db
from history import save_message, load_messages, init_history_db

HOST = '127.0.0.1'
PORT = 9090

clients = {}  # username -> socket


def broadcast(message, sender_username, exclude_sender=False):
    for username, conn in list(clients.items()):
        if exclude_sender and username == sender_username:
            continue
        try:
            conn.sendall(message)
        except:
            conn.close()
            del clients[username]


def handle_file_transfer(conn, sender, metadata):
    try:
        parts = metadata.split("|", 4)
        if len(parts) != 4:
            return

        _, sender, filename, size_str = parts
        size = int(size_str)

        conn.sendall(b"READY")  # tell sender to send file content

        # receive file data
        received = b""
        while len(received) < size:
            chunk = conn.recv(min(4096, size - len(received)))
            if not chunk:
                break
            received += chunk

        # prepare file header to send to recipients
        file_header = f"FILE|{sender}|{filename}|{size}".encode()

        for user, client_conn in list(clients.items()):
            if user != sender:
                try:
                    client_conn.sendall(file_header)
                    ack = client_conn.recv(5)
                    if ack == b"READY":
                        client_conn.sendall(received)
                except Exception as e:
                    print(f"[ERROR] Sending file to {user}: {e}")
                    client_conn.close()
                    del clients[user]

    except Exception as e:
        print(f"[FILE TRANSFER ERROR] {sender}: {e}")


def client_handler(conn, addr):
    print(f"[NEW] Connection from {addr}", flush=True)
    user = None

    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break

            try:
                decoded = data.decode()
            except UnicodeDecodeError:
                continue

            if decoded.startswith("REGISTER "):
                _, username, password = decoded.strip().split(" ", 2)
                response = handle_register(username, password)
                conn.send(response.encode())

            elif decoded.startswith("LOGIN "):
                _, username, password = decoded.strip().split(" ", 2)
                response = handle_login(username, password)
                if response == "LOGIN_SUCCESS":
                    user = username
                    clients[user] = conn
                conn.send(response.encode())

            elif decoded.startswith("TEXT|"):
                parts = decoded.split("|", 2)
                if len(parts) == 3:
                    sender, encrypted_msg = parts[1], parts[2]
                    save_message(sender, "", encrypted_msg)  # storing encrypted msg
                    broadcast(decoded.encode(), user, exclude_sender=True)

            elif decoded.startswith("FILE|"):
                handle_file_transfer(conn, user, decoded)

            elif decoded.startswith("HISTORY|"):
                parts = decoded.split("|", 1)
                if len(parts) == 2:
                    username = parts[1]
                    messages = load_messages(username)
                    for sender, message, _ in messages:
                        line = f"TEXT|{sender}|{message}"
                        try:
                            conn.sendall(line.encode())
                        except:
                            continue

    except Exception as e:
        print(f"[ERROR] {addr} -> {e}", flush=True)

    finally:
        if user and user in clients:
            del clients[user]
        conn.close()
        print(f"[DISCONNECTED] {addr}", flush=True)


def start_server():
    print("[INFO] Initializing database...", flush=True)
    init_db()
    init_history_db()
    print("[SERVER] History DB initialized.")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[SERVER RUNNING] {HOST}:{PORT}", flush=True)

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr), daemon=True)
        thread.start()


if __name__ == "__main__":
    start_server()
