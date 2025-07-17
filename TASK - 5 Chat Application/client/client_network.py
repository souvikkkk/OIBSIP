import socket
import threading
import os
from plyer import notification  # ✅ Cross-platform notifications
from security import encrypt_message, decrypt_message  # ✅ Encryption functions

HOST = '127.0.0.1'
PORT = 9090

class ChatClient:
    def __init__(self, username, password, on_receive):
        self.username = username
        self.password = password
        self.on_receive = on_receive
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
            login_data = f"LOGIN {self.username} {self.password}"
            print(f"[CLIENT] Sending: {login_data}")
            self.sock.sendall(login_data.encode())
            response = self.sock.recv(1024).decode()
            print(f"[CLIENT] Received: {response}")
            if response == "LOGIN_SUCCESS":
                self.running = True
                thread = threading.Thread(target=self.receive_messages, daemon=True)
                thread.start()
                return True
        except Exception as e:
            print("[ERROR] Could not connect:", e)
        return False

    def send(self, message):
        try:
            self.sock.send(message.encode())
        except Exception as e:
            print("[SEND ERROR]", e)

    def send_text(self, message):
        try:
            encrypted = encrypt_message(message)
            data = f"TEXT|{self.username}|{encrypted}"
            self.sock.sendall(data.encode())
        except Exception as e:
            print("[SEND ERROR]", e)

    def send_file(self, file_path):
        try:
            with open(file_path, "rb") as f:
                file_data = f.read()
            filename = os.path.basename(file_path)
            file_size = len(file_data)

            header = f"FILE|{self.username}|{filename}|{file_size}"
            self.sock.sendall(header.encode())

            ack = self.sock.recv(5)
            if ack == b"READY":
                self.sock.sendall(file_data)
            else:
                print("[FILE SEND ERROR] Server did not ACK with READY")
        except Exception as e:
            print("[FILE SEND ERROR]", e)

    def receive_messages(self):
        try:
            while self.running:
                data = self.sock.recv(4096)
                if not data:
                    break

                try:
                    decoded = data.decode()

                    if decoded.startswith("TEXT|"):
                        parts = decoded.split("|", 2)
                        if len(parts) == 3:
                            sender, encrypted_msg = parts[1], parts[2]
                            try:
                                decrypted = decrypt_message(encrypted_msg)
                            except Exception as e:
                                print("[DECRYPTION ERROR]", e)
                                decrypted = "[UNABLE TO DECRYPT]"

                            # Show notification
                            notification.notify(
                                title=f"Message from {sender}",
                                message=decrypted,
                                timeout=5
                            )

                            # Display in GUI
                            self.on_receive(sender, decrypted)

                    elif decoded.startswith("FILE|"):
                        parts = decoded.split("|", 4)
                        if len(parts) == 4:
                            sender, filename, size = parts[1], parts[2], int(parts[3])
                            self.sock.send(b"READY")
                            file_data = b""
                            while len(file_data) < size:
                                chunk = self.sock.recv(min(4096, size - len(file_data)))
                                if not chunk:
                                    break
                                file_data += chunk
                            self.save_file(filename, file_data)

                            # Show notification
                            notification.notify(
                                title=f"File from {sender}",
                                message=filename,
                                timeout=5
                            )

                            self.on_receive(sender, f"[FILE] {filename}")

                except UnicodeDecodeError:
                    print("[CLIENT] Received binary data")

        except Exception as e:
            print("[RECEIVE ERROR]", e)

    def save_file(self, filename, data):
        os.makedirs("client_downloads", exist_ok=True)
        path = os.path.join("client_downloads", filename)
        with open(path, "wb") as f:
            f.write(data)
