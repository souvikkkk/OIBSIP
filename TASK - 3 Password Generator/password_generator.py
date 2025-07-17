import tkinter as tk
from tkinter import messagebox
import string
import secrets
import pyperclip

def generate_password():
    length = length_var.get()
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_symbols = symbols_var.get()

    if not (use_upper or use_lower or use_digits or use_symbols):
        messagebox.showerror("Error", "Select at least one character set!")
        return

    char_sets = []
    if use_upper:
        char_sets.append(string.ascii_uppercase)
    if use_lower:
        char_sets.append(string.ascii_lowercase)
    if use_digits:
        char_sets.append(string.digits)
    if use_symbols:
        char_sets.append(string.punctuation)

    all_chars = ''.join(char_sets)

    password = [secrets.choice(s) for s in char_sets]

    if length < len(password):
        messagebox.showerror("Error", f"Length must be at least {len(password)} to include all selected sets.")
        return

    password += [secrets.choice(all_chars) for _ in range(length - len(password))]
    secrets.SystemRandom().shuffle(password)

    final_password = ''.join(password)
    generated_password.set(final_password)
    strength_label.config(text=f"Strength: {assess_strength(final_password)}")

def assess_strength(pw):
    length = len(pw)
    score = 0
    if any(c.islower() for c in pw):
        score += 1
    if any(c.isupper() for c in pw):
        score += 1
    if any(c.isdigit() for c in pw):
        score += 1
    if any(c in string.punctuation for c in pw):
        score += 1
    if length >= 12:
        score += 1
    if length >= 16:
        score += 1

    if score <= 2:
        return "Weak"
    elif score <= 4:
        return "Medium"
    else:
        return "Strong"

def copy_to_clipboard():
    pw = generated_password.get()
    if pw:
        pyperclip.copy(pw)
        messagebox.showinfo("Copied", "Password copied to clipboard!")

def save_to_file():
    pw = generated_password.get()
    if not pw:
        messagebox.showwarning("Warning", "Generate a password first.")
        return
    with open("saved_passwords.txt", "a") as f:
        f.write(pw + "\n")
    messagebox.showinfo("Saved", "Password saved to saved_passwords.txt")

# Tooltip helper
def create_tooltip(widget, text):
    tooltip = tk.Toplevel(widget)
    tooltip.withdraw()
    tooltip.overrideredirect(True)
    label = tk.Label(
        tooltip,
        text=text,
        background="#333",
        foreground="white",
        relief="solid",
        borderwidth=1,
        padx=4,
        pady=2,
        font=("Arial", 9)
    )
    label.pack()
    
    def enter(event):
        x = event.x_root + 10
        y = event.y_root + 10
        tooltip.geometry(f"+{x}+{y}")
        tooltip.deiconify()
        
    def leave(event):
        tooltip.withdraw()
        
    widget.bind("<Enter>", enter)
    widget.bind("<Leave>", leave)

# GUI
root = tk.Tk()
root.title("🌟 Advanced Password Generator")
root.configure(bg="#2c3e50")
root.geometry("460x450")
root.resizable(False, False)

length_var = tk.IntVar(value=12)
upper_var = tk.BooleanVar(value=True)
lower_var = tk.BooleanVar(value=True)
digits_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=False)
generated_password = tk.StringVar()

# Title
title_label = tk.Label(
    root,
    text="🌟 Advanced Password Generator",
    font=("Helvetica", 18, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1",
    pady=10
)
title_label.pack()

frame = tk.Frame(root, bg="#34495e", padx=10, pady=10, bd=1, relief="groove")
frame.pack(pady=10, padx=15, fill="x")

tk.Label(frame, text="Password Length:", font=("Arial", 11), bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, sticky="w")
spin = tk.Spinbox(frame, from_=4, to=64, textvariable=length_var, width=5, font=("Arial", 11))
spin.grid(row=0, column=1, sticky="w")
create_tooltip(spin, "Select password length")

# Checkboxes
checks = [
    (upper_var, "Include Uppercase"),
    (lower_var, "Include Lowercase"),
    (digits_var, "Include Digits"),
    (symbols_var, "Include Symbols"),
]
for i, (var, text) in enumerate(checks, 1):
    cb = tk.Checkbutton(
        frame,
        text=text,
        variable=var,
        font=("Arial", 11),
        bg="#34495e",
        fg="#ecf0f1",
        activebackground="#34495e",
        selectcolor="#16a085"
    )
    cb.grid(row=i, column=0, columnspan=2, sticky="w")
    create_tooltip(cb, text)

# Generate Button
generate_btn = tk.Button(
    root,
    text="Generate Password",
    command=generate_password,
    bg="#27ae60",
    fg="white",
    activebackground="#2ecc71",
    font=("Arial", 13),
    bd=0,
    padx=10,
    pady=5
)
generate_btn.pack(pady=10)

# Output Entry
entry = tk.Entry(
    root,
    textvariable=generated_password,
    font=("Courier", 14),
    justify="center",
    bg="#ecf0f1",
    relief="sunken",
    bd=2
)
entry.pack(padx=15, fill="x", pady=5)

strength_label = tk.Label(
    root,
    text="Strength: N/A",
    font=("Arial", 11, "bold"),
    bg="#2c3e50",
    fg="#ecf0f1"
)
strength_label.pack()

# Buttons Frame
button_frame = tk.Frame(root, bg="#2c3e50")
button_frame.pack(pady=15)

copy_btn = tk.Button(
    button_frame,
    text="📋 Copy",
    command=copy_to_clipboard,
    bg="#2980b9",
    fg="white",
    activebackground="#3498db",
    font=("Arial", 11),
    padx=10,
    pady=4,
    bd=0
)
copy_btn.grid(row=0, column=0, padx=5)
create_tooltip(copy_btn, "Copy password to clipboard")

save_btn = tk.Button(
    button_frame,
    text="💾 Save",
    command=save_to_file,
    bg="#8e44ad",
    fg="white",
    activebackground="#9b59b6",
    font=("Arial", 11),
    padx=10,
    pady=4,
    bd=0
)
save_btn.grid(row=0, column=1, padx=5)
create_tooltip(save_btn, "Save password to file")

root.mainloop()
