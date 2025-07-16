# gaze_tracker.py
import cv2
import time
from gaze_tracking import GazeTracking
from PIL import Image

def track_gaze(stimuli, running_flag, callback):
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    prev_state = None

    for label, img_path in stimuli:
        if not running_flag.is_set():
            break

        frame_img = cv2.imread(img_path)
        if frame_img is None:
            print(f"Could not load image: {img_path}")
            continue

        # Convert to Tk-compatible Image and send to GUI
        rgb_img = cv2.cvtColor(frame_img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(rgb_img)
        callback(("stimulus", label, pil_img))

        start_time = time.time()
        while time.time() - start_time < 3 and running_flag.is_set():
            ret, frame = webcam.read()
            if not ret:
                continue

            gaze.refresh(frame)

            if gaze.is_blinking():
                current_state = "Blinking"
            elif gaze.is_right():
                current_state = "Looking Right"
            elif gaze.is_left():
                current_state = "Looking Left"
            elif gaze.is_center():
                current_state = "Looking Center"
            else:
                current_state = "Undetected"

            if current_state != prev_state:
                timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                left_pupil = gaze.pupil_left_coords()
                right_pupil = gaze.pupil_right_coords()
                callback([timestamp, label, current_state, left_pupil, right_pupil])
                prev_state = current_state

    webcam.release()



