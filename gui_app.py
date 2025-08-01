#gui_app.py

import tkinter as tk
from tkinter import messagebox, simpledialog
import threading
import pandas as pd
from PIL import Image, ImageTk
from gaze_tracker import track_gaze
from gaze_tracking import GazeTracking
import matplotlib.pyplot as plt
import cv2
import re
import time

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




def preview_gaze_tracking():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    if not webcam.isOpened():
        messagebox.showerror("Preview", "Webcam not accessible.")
        return

    cv2.namedWindow("Preview - Gaze Tracking", cv2.WINDOW_NORMAL)
    print("[Preview] Press ESC or close the window to exit preview.")

    while True:
        ret, frame = webcam.read()
        if not ret:
            continue

        gaze.refresh(frame)
        annotated_frame = gaze.annotated_frame()
        cv2.imshow("Preview - Gaze Tracking", annotated_frame)

        key = cv2.waitKey(1)
        if key == 27:  # ESC pressed
            break

        # Check if the window was manually closed
        try:
            if cv2.getWindowProperty("Preview - Gaze Tracking", cv2.WND_PROP_VISIBLE) < 1:
                break
        except cv2.error:
            break

    # Clean up
    webcam.release()
    time.sleep(0.1)
    cv2.destroyAllWindows()
    time.sleep(0.1)



def start_tracking():
    global tracking_thread, running_flag
    if tracking_thread and tracking_thread.is_alive():
        messagebox.showinfo("Tracking", "Tracking is already running.")
        return
    gaze_data.clear()  # <-- reset for new session
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
    try:
        df = pd.DataFrame(
            gaze_data,
            columns=["Timestamp", "Stimulus", "Gaze State", "Left Pupil", "Right Pupil", "Pupil Distance (mm)"]
        )
        df.to_csv("gaze_log.csv", index=False)
        messagebox.showinfo("Export", "Data exported to gaze_log.csv")
    except Exception as e:
        messagebox.showerror("Export Error", str(e))


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
    import cv2
    from tkinter import messagebox, simpledialog

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[Calibration] Webcam not accessible.")
        return None

    print("[Calibration] Press SPACE to capture image, or ESC to cancel.")
    messagebox.showinfo(
        "Calibration - Step 1",
        "Live camera feed will open.\n\n"
        "➡ Press SPACE to capture an image\n"
        "➡ Press ESC to cancel."
    )

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        cv2.imshow("Live Preview - Press SPACE to capture", frame)
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            print("[Calibration] Cancelled.")
            cap.release()
            cv2.destroyAllWindows()
            return None
        elif key == 32:  # SPACE
            print("[Calibration] Image captured.")
            break

    cap.release()
    cv2.destroyWindow("Live Preview - Press SPACE to capture")

    points = []

    def on_click(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN and len(points) < 2:
            points.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow("Calibration - Click 2 Points", frame)

    messagebox.showinfo(
        "Calibration - Step 2",
        "Click two points on the image to measure known distance.\n\n"
        "➡ Press ENTER when done\n"
        "➡ Press ESC to cancel"
    )

    print("[Calibration] Click two points. Press ENTER when done, ESC to cancel.")
    cv2.namedWindow("Calibration - Click 2 Points", cv2.WINDOW_NORMAL)
    cv2.setMouseCallback("Calibration - Click 2 Points", on_click)
    cv2.imshow("Calibration - Click 2 Points", frame)

    while True:
        key = cv2.waitKey(1)
        if key == 27:  # ESC
            print("[Calibration] Cancelled by user.")
            cv2.destroyAllWindows()
            return None
        elif key == 13 and len(points) == 2:  # ENTER
            break

    cv2.destroyAllWindows()

    dx = points[1][0] - points[0][0]
    dy = points[1][1] - points[0][1]
    pixel_dist = (dx ** 2 + dy ** 2) ** 0.5

    return pixel_dist





def handle_calibration():
    pixel_dist = run_calibration()
    if pixel_dist:
        mm_dist = simpledialog.askfloat("Input", "Enter real-world distance in mm between the two points:")
        if mm_dist and mm_dist > 0:
            scale = mm_dist / pixel_dist
            with open("calibration.txt", "w") as f:
                f.write(f"{scale}")
            print(f"[Calibration] Saved scale: {scale:.4f} mm/pixel")
            messagebox.showinfo("Calibration", f"Saved scale: {scale:.4f} mm/pixel")
        else:
            print("[Calibration] Invalid or cancelled mm input.")
    else:
        print("[Calibration] No pixel distance measured.")



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

tk.Button(root, text="Preview Gaze Tracking", command=preview_gaze_tracking).pack(pady=5)
tk.Button(root, text="Start", command=start_tracking).pack(pady=2)
tk.Button(root, text="Stop", command=stop_tracking).pack(pady=2)
tk.Button(root, text="Export CSV", command=export_data).pack(pady=5)
tk.Button(root, text="Plot Data", command=plot_data).pack(pady=5)
tk.Button(root, text="Plot Pupil Positions", command=plot_pupil_positions).pack(pady=5)
tk.Button(root, text="Calibrate Scale (mm/pixel)", command=handle_calibration).pack(pady=5)

root.mainloop()

