# client/chat_list.py

import tkinter as tk
from chat_ui import launch_chat

def open_room(username, password, partner_name):
    launch_chat(username, password, partner_name)


def show_chat_list(username, password):
    window = tk.Tk()
    window.title(f"{username} - Chat List")
    window.geometry("400x500")
    window.configure(bg="#f0f2f5")

    title = tk.Label(window, text="Your Chats", font=("Segoe UI", 14, "bold"),
                     bg="#075E54", fg="white", padx=10, pady=10)
    title.pack(fill=tk.X)

    frame = tk.Frame(window, bg="#f0f2f5")
    frame.pack(fill=tk.BOTH, expand=True)

    # Placeholder: static rooms for now
    room_names = ["Friends", "Family", "Work", "Random"]
    for room in room_names:
        btn = tk.Button(frame, text=room, font=("Segoe UI", 12),
                        bg="white", fg="black", anchor='w',
                        command=lambda r=room: [window.destroy(), open_room(username, password, room)])
        btn.pack(fill=tk.X, padx=20, pady=6, ipadx=10, ipady=6)

    # Join/Create new room
    entry_label = tk.Label(window, text="Join or Create Room:", bg="#f0f2f5", fg="black", font=("Segoe UI", 10))
    entry_label.pack(pady=(10, 0))

    room_entry = tk.Entry(window, font=("Segoe UI", 11))
    room_entry.pack(pady=6, padx=20, fill=tk.X)

    def join_custom_room():
        room = room_entry.get().strip()
        if room:
            window.destroy()
            open_room(username,password, room)

    join_btn = tk.Button(window, text="Enter Room", font=("Segoe UI", 10),
                         bg="#25D366", fg="white", relief='flat',
                         command=join_custom_room)
    join_btn.pack(pady=10)

    window.mainloop()
