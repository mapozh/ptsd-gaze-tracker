# gui_app.py
import tkinter as tk
from tkinter import messagebox
import threading
import pandas as pd
from PIL import Image, ImageTk
from gaze_tracker import track_gaze

gaze_data = []

def ui_callback(data):
    if isinstance(data, tuple) and data[0] == "stimulus":
        # Update stimulus image and label
        label, img = data[1], data[2]
        stimulus_var.set(f"Stimulus: {label}")
        tk_image = ImageTk.PhotoImage(img)
        canvas.img = tk_image  # Prevent garbage collection
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    else:
        # Append gaze data
        gaze_data.append(data)
        gaze_var.set(f"Gaze: {data[2]}")

def start_tracking():
    global tracking_thread, running_flag
    if tracking_thread and tracking_thread.is_alive():
        return
    running_flag.set()
    tracking_thread = threading.Thread(
        target=track_gaze,
        args=(stimuli, running_flag, ui_callback),
        daemon=True
    )
    tracking_thread.start()

def stop_tracking():
    running_flag.clear()

def export_data():
    if not gaze_data:
        messagebox.showwarning("Export", "No data to export.")
        return
    df = pd.DataFrame(gaze_data, columns=["Timestamp", "Stimulus", "Gaze State", "Left Pupil", "Right Pupil"])
    df.to_csv("gaze_log.csv", index=False)
    messagebox.showinfo("Export", "Data exported to gaze_log.csv")

# --- GUI Setup ---
stimuli = [
    ("neutral", "stimuli/neutral.jpg"),
    ("threat", "stimuli/threat.jpg"),
    ("happy", "stimuli/happy.jpg")
]

tracking_thread = None
running_flag = threading.Event()

root = tk.Tk()
root.title("Gaze Tracker")

stimulus_var = tk.StringVar(value="Stimulus: ")
gaze_var = tk.StringVar(value="Gaze: ")

tk.Label(root, textvariable=stimulus_var, font=("Arial", 14)).pack(pady=5)
tk.Label(root, textvariable=gaze_var, font=("Arial", 14)).pack(pady=5)

canvas = tk.Canvas(root, width=640, height=360, bg="gray")
canvas.pack(pady=10)

tk.Button(root, text="Start", command=start_tracking).pack(pady=2)
tk.Button(root, text="Stop", command=stop_tracking).pack(pady=2)
tk.Button(root, text="Export CSV", command=export_data).pack(pady=5)

root.mainloop()

