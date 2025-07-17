# PTSD Pupillometry & Gaze Tracking App

This project is a simple Python-based desktop application that uses **pupillometry** and **gaze tracking** to assist in identifying emotional and physiological responses related to **Post-Traumatic Stress Disorder (PTSD)**.

The app presents short visual stimuli (images) and tracks:

- 👁️ Eye gaze direction  
- ⏱️ Fixation state changes  
- 📌 Pupil position (in pixels or millimeters, if calibrated)

These measurements may help in identifying symptoms such as **threat avoidance**, **hypervigilance**, and **emotional arousal**.

---

## 📦 Features

- ✅ Simple GUI (Tkinter-based) — just one button to start
- 📸 Real-time webcam tracking of gaze and pupil coordinates
- 🧠 Gaze direction & blink detection via [GazeTracking](https://github.com/antoinelame/GazeTracking)
- 📊 Logs pupil position (left & right) and gaze state to CSV
- 📁 Automatic CSV export after session
- 📈 Built-in data visualization (gaze frequency & pupil scatterplots)
- 📐 Manual calibration tool for converting pixels to millimeters

---

## 🧰 Tech Stack

- Python 3.10
- OpenCV
- GazeTracking
- Tkinter (standard GUI library)
- NumPy
- Pandas
- Pillow (for image display in Tkinter)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/ptsd-gaze-tracker.git
cd ptsd-gaze-tracker
```

### 2. Set Up a Virtual Environment (Recommended)

```bash
python3.10 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python gui_app.py
```

### 5. Export CSV Data

After running a session, click **Export CSV** in the GUI.
The file will be saved as `gaze_log.csv` in your project directory, with data like:

```
Timestamp,Stimulus,Gaze State,Left Pupil,Right Pupil
2025-07-16 19:29:11,neutral,Looking Center,"(345, 300)","(398, 299)"
2025-07-16 19:29:12,neutral,Looking Left,"(346, 299)","(399, 298)"
...
```

## 📐 Calibration (Optional but Recommended)

Pupil coordinates and eye features are recorded in **pixels**,  
but researchers often need measurements in **millimeters** for scientific accuracy.  
This app provides a **manual calibration tool** to estimate the scale between real-world distances and pixel units.

### 🔧 How it works:

1. Click the **Calibrate** button in the GUI.
2. A **live webcam preview** opens.
3. Press **SPACE** to capture a still image for calibration.
4. Click **two points** on an object of known length (e.g., marks on a ruler 10 mm apart).
5. Press **ENTER** when done.
6. Enter the actual **distance in mm** when prompted.
7. The app computes and stores the **pixels-per-mm ratio** to `calibration.txt`.

✅ Once calibrated, the app can later convert pixel-based pupil coordinates  
into **millimeter units** — useful for **pupillometry**, **clinical screening**, or **experimental psychology**.

> 🧠 Tip: For best results, use a small physical ruler or caliper in front of the camera during calibration.


---

## Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** this repository
2. **Create a branch:**

   ```bash
   git checkout -b feature-xyz
   ```
3. **Commit your changes:**

   ```bash
   git commit -am 'Add new feature'
   ```
4. **Push to the branch:**

   ```bash
   git push origin feature-xyz
   ```
5. **Create a Pull Request**

Please make sure your code follows the existing style and includes relevant documentation or comments.

