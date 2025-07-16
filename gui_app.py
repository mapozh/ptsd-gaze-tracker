import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import pandas as pd
from PIL import Image, ImageTk
from gaze_tracker import track_gaze
import matplotlib.pyplot as plt
import cv2
import re

gaze_data = []

def ui_callback(data):
    if isinstance(data, tuple) and data[0] == "stimulus":
        label, img = data[1], data[2]
        stimulus_var.set(f"Stimulus: {label}")
        tk_image = ImageTk.PhotoImage(img)
        canvas.img = tk_image
        canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
    else:
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

def plot_data():
    try:
        df = pd.read_csv("gaze_log.csv")
        stimuli = df["Stimulus"].unique()
        fig, axs = plt.subplots(1, len(stimuli), figsize=(6 * len(stimuli), 5))
        if len(stimuli) == 1:
            axs = [axs]
        for ax, stim in zip(axs, stimuli):
            subset = df[df["Stimulus"] == stim]
            state_counts = subset["Gaze State"].value_counts()
            state_counts.plot(kind='bar', ax=ax)
            ax.set_title(f"Gaze State Frequency: {stim}")
            ax.set_xlabel("Gaze State")
            ax.set_ylabel("Count")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Plot Error", str(e))

def plot_pupil_positions():
    try:
        df = pd.read_csv("gaze_log.csv")
        stimuli = df["Stimulus"].unique()
        fig, axs = plt.subplots(1, len(stimuli), figsize=(6 * len(stimuli), 5))
        if len(stimuli) == 1:
            axs = [axs]
        for ax, stim in zip(axs, stimuli):
            subset = df[df["Stimulus"] == stim]
            def extract_coords(s):
                if pd.isna(s):
                    return (None, None)
                match = re.match(r"\(np\.int32\((\d+)\), np\.int32\((\d+)\)\)", s)
                if match:
                    return int(match.group(1)), int(match.group(2))
                return (None, None)
            left_coords = subset["Left Pupil"].apply(extract_coords)
            left_x = [x for x, y in left_coords if x is not None]
            left_y = [y for x, y in left_coords if y is not None]
            ax.scatter(left_x, left_y, alpha=0.6)
            ax.set_title(f"Left Pupil Positions: {stim}")
            ax.set_xlabel("X")
            ax.set_ylabel("Y")
        plt.tight_layout()
        plt.show()
    except Exception as e:
        messagebox.showerror("Plot Error", str(e))

def run_calibration():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Calibration", "Webcam not accessible.")
        return

    ret, frame = cap.read()
    cap.release()

    if not ret:
        messagebox.showerror("Calibration", "Failed to capture image from webcam.")
        return

    points = []

    def on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Calibration", frame)
            if len(points) == 2:
                dx = points[1][0] - points[0][0]
                dy = points[1][1] - points[0][1]
                pixel_dist = (dx ** 2 + dy ** 2) ** 0.5
                cv2.destroyWindow("Calibration")
                cv2.waitKey(1)  # Prevent segfault
                mm_dist = simpledialog.askfloat("Input", "Enter real-world distance in mm between the two points:")
                if mm_dist and mm_dist > 0:
                    scale = mm_dist / pixel_dist
                    with open("calibration.txt", "w") as f:
                        f.write(f"{scale}")
                    messagebox.showinfo("Calibration", f"Saved scale: {scale:.4f} mm/pixel")
                    print(f"[Calibration] Saved scale: {scale:.4f} mm/pixel")

    messagebox.showinfo("Calibration", "Click two points on the image to measure a known real-world distance.")
    cv2.namedWindow("Calibration", cv2.WINDOW_NORMAL)
    cv2.imshow("Calibration", frame)
    cv2.setMouseCallback("Calibration", on_click)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)


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
tk.Button(root, text="Plot Data", command=plot_data).pack(pady=5)
tk.Button(root, text="Plot Pupil Positions", command=plot_pupil_positions).pack(pady=5)
tk.Button(root, text="Calibrate Pupil Size", command=run_calibration).pack(pady=5)

root.mainloop()

