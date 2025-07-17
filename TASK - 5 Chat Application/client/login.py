import tkinter as tk
from tkinter import messagebox
from handlers import send_request
from chat_list import show_chat_list  # ✅ Correct: go to room selector after login

def LoginWindow():
    window = tk.Tk()
    window.title("Login")
    window.geometry("350x300")
    window.configure(bg="#f0f2f5")

    title = tk.Label(window, text="Chat Login", font=("Segoe UI", 16, "bold"), bg="#075E54", fg="white")
    title.pack(fill=tk.X, pady=(0, 20))

    frame = tk.Frame(window, bg="#f0f2f5")
    frame.pack(pady=10)

    tk.Label(frame, text="Username:", font=("Segoe UI", 12), bg="#f0f2f5").grid(row=0, column=0, sticky="w", pady=8)
    username_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25)
    username_entry.grid(row=0, column=1, pady=8)

    tk.Label(frame, text="Password:", font=("Segoe UI", 12), bg="#f0f2f5").grid(row=1, column=0, sticky="w", pady=8)
    password_entry = tk.Entry(frame, font=("Segoe UI", 11), width=25, show="*")
    password_entry.grid(row=1, column=1, pady=8)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "Please enter both username and password.")
            return

        result = send_request("LOGIN", username, password)
        if result == "LOGIN_SUCCESS":
            window.destroy()
            show_chat_list(username, password)  # ✅ Corrected here
        else:
            messagebox.showerror("Login Failed", result)


    def register():
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Error", "All fields are required.")
            return

        response = send_request("REGISTER", username, password)
        if response == "REGISTER_SUCCESS":
            messagebox.showinfo("Success", "Registered successfully. You can now log in.")
        else:
            messagebox.showerror("Failed", "Registration failed. Username might already exist.")

    btn_frame = tk.Frame(window, bg="#f0f2f5")
    btn_frame.pack(pady=20)

    login_btn = tk.Button(btn_frame, text="Login", font=("Segoe UI", 10, "bold"),
                          bg="#25D366", fg="white", width=12, relief='flat', command=login)
    login_btn.grid(row=0, column=0, padx=10)

    register_btn = tk.Button(btn_frame, text="Register", font=("Segoe UI", 10, "bold"),
                             bg="#128C7E", fg="white", width=12, relief='flat', command=register)
    register_btn.grid(row=0, column=1, padx=10)

    window.mainloop()
