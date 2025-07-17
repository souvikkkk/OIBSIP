import tkinter as tk
from tkinter import filedialog, messagebox
from client_network import ChatClient
import os
import webbrowser
import emoji
from history import load_messages, save_message

MAX_INPUT_LINES = 5

def launch_chat(username, password, partner):
    root = tk.Tk()
    root.title(f"Chat - {username} chatting with {partner}")
    root.geometry("600x600")
    root.configure(bg="#111B21")

    client = None
    chat_display = None

    def on_message_received(sender, message):
        display_message(sender, message)
        if not message.startswith("[FILE]"):
            save_message(sender, partner, message)

    def display_message(sender, message):
        is_self = sender == username
        bubble = tk.Frame(chat_display, bg="#111B21")
        bubble.pack(anchor='e' if is_self else 'w', padx=10, pady=2, fill="x")

        color = "#25D366" if is_self else "#2A3942"
        align = "e" if is_self else "w"

        if message.startswith("[FILE]"):
            filename = message.split("[FILE] ")[1]
            file_path = os.path.abspath(os.path.join("client_downloads", filename))
            btn = tk.Button(bubble, text=f"📎 {filename}", bg=color, fg="white", font=("Segoe UI", 10),
                            anchor=align, relief="flat", command=lambda: open_file(file_path))
            btn.pack(anchor=align, padx=8, pady=4)
        else:
            msg_label = tk.Label(
                bubble,
                text=emoji.emojize(message),
                wraplength=400,
                justify="left",
                bg=color,
                fg="white",
                font=("Segoe UI", 11),
                padx=10,
                pady=6
            )
            msg_label.pack(anchor=align)

        chat_canvas.update_idletasks()
        chat_canvas.yview_moveto(1.0)

    def open_file(path):
        try:
            webbrowser.open(path)
        except:
            messagebox.showerror("Error", "Could not open file.")

    # Top Frame
    top_frame = tk.Frame(root, bg="#202C33", height=50)
    top_frame.pack(side="top", fill="x")
    tk.Label(top_frame, text=f"{partner}", fg="white", bg="#202C33",
             font=("Segoe UI", 12, "bold"), padx=15).pack(anchor="w")

    # Chat area
    chat_frame = tk.Frame(root, bg="#111B21")
    chat_frame.pack(fill="both", expand=True)

    chat_canvas = tk.Canvas(chat_frame, bg="#111B21", bd=0, highlightthickness=0)
    scrollbar = tk.Scrollbar(chat_frame, command=chat_canvas.yview)
    chat_display = tk.Frame(chat_canvas, bg="#111B21")

    chat_display.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
    chat_canvas.create_window((0, 0), window=chat_display, anchor="nw")
    chat_canvas.configure(yscrollcommand=scrollbar.set)

    chat_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Bottom input area
    input_frame = tk.Frame(root, bg="#202C33", height=50)
    input_frame.pack(side="bottom", fill="x")

    def auto_resize(event=None):
        lines = int(text_input.index("end-1c").split('.')[0])
        lines = min(lines, MAX_INPUT_LINES)
        text_input.config(height=lines)

    text_input = tk.Text(input_frame, height=2, wrap="word", font=("Segoe UI", 11),
                         bg="#2A3942", fg="white", relief="flat")
    text_input.pack(side="left", fill="both", expand=True, padx=(8, 4), pady=8)
    text_input.bind("<KeyRelease>", auto_resize)

    def handle_send(event=None):
        message = text_input.get("1.0", tk.END).strip()
        if message:
            client.send_text(message)
            display_message(username, message)
            save_message(username, partner, message)
            text_input.delete("1.0", tk.END)
            auto_resize()

    def handle_file():
        file_path = filedialog.askopenfilename()
        if file_path:
            client.send_file(file_path)
            filename = os.path.basename(file_path)
            display_message(username, f"[FILE] {filename}")
            save_message(username, partner, f"[FILE] {filename}")

    send_btn = tk.Button(input_frame, text="➤", font=("Segoe UI", 14), command=handle_send,
                         bg="#0B8457", fg="white", relief="flat", width=4)
    send_btn.pack(side="right", padx=8)

    file_btn = tk.Button(input_frame, text="📎", font=("Segoe UI", 12), command=handle_file,
                         bg="#202C33", fg="white", relief="flat", width=3)
    file_btn.pack(side="right")

    emoji_btn = tk.Button(input_frame, text="😊", font=("Segoe UI", 12),
                          bg="#202C33", fg="white", relief="flat", width=3,
                          command=lambda: text_input.insert(tk.END, emoji.emojize(":smile:")))
    emoji_btn.pack(side="right")

    # Connect to server
    client = ChatClient(username, password, on_message_received)
    if not client.connect():
        messagebox.showerror("Connection Error", "Could not connect to server.")
        root.destroy()
        return

    # Load chat history
    try:
        history = load_messages(username, partner)
        for sender, msg, _ in history:
            display_message(sender, msg)
    except Exception as e:
        print("[HISTORY LOAD ERROR]", e)

    root.bind("<Return>", lambda e: handle_send())
    root.mainloop()
