import cv2
import csv
import time
from gaze_tracking import GazeTracking

def main():
    gaze = GazeTracking()
    webcam = cv2.VideoCapture(0)

    stimuli = [
        ("neutral", "stimuli/neutral.jpg"),
        ("threat", "stimuli/threat.jpg"),
        ("happy", "stimuli/happy.jpg")
    ]

    prev_state = None

    with open("gaze_log.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Stimulus", "Gaze State", "Left Pupil", "Right Pupil"])

        print("Press 'q' to quit at any time.")

        for label, image_path in stimuli:
            stimulus_img = cv2.imread(image_path)
            if stimulus_img is None:
                print(f"Failed to load {image_path}")
                continue

            print(f"Showing: {label}")

            start_time = time.time()
            while time.time() - start_time < 3:  # Show for 3 seconds
                _, frame = webcam.read()
                gaze.refresh(frame)

                # show stimulus window
                cv2.imshow("Stimulus", stimulus_img)

                # Check for quit key
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    webcam.release()
                    cv2.destroyAllWindows()
                    return

                # Determine gaze state
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

                # Log if state changes
                if current_state != prev_state:
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                    left_pupil = gaze.pupil_left_coords()
                    right_pupil = gaze.pupil_right_coords()
                    writer.writerow([timestamp, label, current_state, left_pupil, right_pupil])
                    print(f"[{timestamp}] {label} → {current_state}")
                    prev_state = current_state

    webcam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

    # Optional: show CSV contents
    import pandas as pd
    df = pd.read_csv("gaze_log.csv")
    print(df)
