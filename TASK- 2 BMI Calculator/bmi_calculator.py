import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import os
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

root = tk.Tk()
root.withdraw()

username = simpledialog.askstring("User Login", "Enter your username:")

if not username:
    messagebox.showerror("Error", "Username is required.")
    exit()

DATA_FILE = f"bmi_data_{username.lower()}.txt"

root.deiconify()
root.title(f"BMI Calculator - User: {username}")
root.geometry("700x450")
root.configure(bg="#f0f4f7")

# Style
style = ttk.Style()
style.theme_use("clam")

style.configure("TFrame", background="#f0f4f7")
style.configure("TLabel", font=("Segoe UI", 12), background="#f0f4f7", foreground="#333")
style.configure("TButton", font=("Segoe UI", 12), padding=6)
style.configure("TEntry", font=("Segoe UI", 12))

# Functions
def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height_cm = float(entry_height.get())
        if weight <= 0 or height_cm <= 0:
            messagebox.showerror("Input Error", "Weight and height must be positive numbers.")
            return

        height_m = height_cm / 100
        bmi = weight / (height_m ** 2)
        category = get_bmi_category(bmi)
        label_result.config(text=f"BMI: {bmi:.2f}\nCategory: {category}")

        save_bmi(datetime.now().strftime("%Y-%m-%d %H:%M"), weight, height_cm, bmi, category)
        update_plot()
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 24.9:
        return "Normal weight"
    elif 25 <= bmi < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def save_bmi(date, weight, height, bmi, category):
    with open(DATA_FILE, "a") as f:
        f.write(
            f"Date: {date}\n"
            f"Weight: {weight} kg\n"
            f"Height: {height} cm\n"
            f"BMI: {round(bmi, 2)}\n"
            f"Category: {category}\n"
            "-----------------------------\n"
        )

def show_frame(frame):
    frame.tkraise()

def update_plot():
    for widget in frame_history_content.winfo_children():
        widget.destroy()

    if not os.path.exists(DATA_FILE):
        ttk.Label(frame_history_content, text="No BMI history available.").pack()
        return

    # Parse the .txt file
    dates = []
    bmis = []

    with open(DATA_FILE, "r") as f:
        lines = f.readlines()

    current_date = None
    current_bmi = None

    for line in lines:
        line = line.strip()
        if line.startswith("Date:"):
            current_date = line.replace("Date:","").strip()
        elif line.startswith("BMI:"):
            current_bmi = float(line.replace("BMI:","").strip())
        elif line.startswith("-----------------------------"):
            if current_date and current_bmi is not None:
                dates.append(current_date)
                bmis.append(current_bmi)
            current_date = None
            current_bmi = None

    if not dates:
        ttk.Label(frame_history_content, text="No BMI data to plot.").pack()
        return

    # Create plot
    fig, ax = plt.subplots(figsize=(5,3))
    ax.plot(dates, bmis, marker="o")
    ax.set_xlabel("Date")
    ax.set_ylabel("BMI")
    ax.set_title(f"{username}'s BMI Over Time")
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame_history_content)
    canvas.draw()
    canvas.get_tk_widget().pack()

# Layout: 2 columns
frame_sidebar = ttk.Frame(root, width=150)
frame_sidebar.pack(side="left", fill="y")

frame_main = ttk.Frame(root)
frame_main.pack(side="right", fill="both", expand=True)

# Sidebar Buttons
btn_calc = ttk.Button(frame_sidebar, text="BMI Calculator", command=lambda: show_frame(frame_calc))
btn_calc.pack(fill="x", pady=5, padx=5)

btn_history = ttk.Button(frame_sidebar, text="BMI History", command=lambda: [show_frame(frame_history), update_plot()])
btn_history.pack(fill="x", pady=5, padx=5)

# Frames to switch
frame_calc = ttk.Frame(frame_main)
frame_history = ttk.Frame(frame_main)

for frame in (frame_calc, frame_history):
    frame.place(relwidth=1, relheight=1)

# BMI Calculator Frame Content
frame_calc_content = ttk.Frame(frame_calc)
frame_calc_content.place(relx=0.5, rely=0.4, anchor="center")

ttk.Label(frame_calc_content, text="Enter your weight (kg):").grid(row=0, column=0, sticky="W", pady=8)
entry_weight = ttk.Entry(frame_calc_content, width=25)
entry_weight.grid(row=0, column=1, pady=8)

ttk.Label(frame_calc_content, text="Enter your height (cm):").grid(row=1, column=0, sticky="W", pady=8)
entry_height = ttk.Entry(frame_calc_content, width=25)
entry_height.grid(row=1, column=1, pady=8)

btn_calc_bmi = ttk.Button(frame_calc_content, text="Calculate BMI", command=calculate_bmi)
btn_calc_bmi.grid(row=2, column=0, columnspan=2, pady=15)

label_result = ttk.Label(frame_calc_content, text="", font=("Segoe UI", 12, "bold"))
label_result.grid(row=3, column=0, columnspan=2, pady=10)

# BMI History Frame
frame_history_content = ttk.Frame(frame_history)
frame_history_content.pack(fill="both", expand=True, padx=10, pady=10)

# Show calculator frame by default
show_frame(frame_calc)

root.mainloop()
