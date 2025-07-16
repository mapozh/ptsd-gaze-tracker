# PTSD Pupillometry & Gaze Tracking App

This project is a simple Python-based desktop application that uses **pupillometry** and **gaze tracking** to assist in identifying emotional and physiological responses related to **Post-Traumatic Stress Disorder (PTSD)**.

The app presents short visual stimuli (images) and tracks:

- 👁️ Eye gaze direction  
- ⏱️ Fixation duration  
- 🎯 Pupil size changes  

These measurements may help in identifying symptoms such as **threat avoidance**, **hypervigilance**, and **emotional arousal**.

---

## 📦 Features

- ✅ One-button start GUI (Tkinter-based)
- 📸 Real-time webcam tracking
- 🧠 Gaze & blink detection with [GazeTracking](https://github.com/antoinelame/GazeTracking)
- 📊 Pupil position logging
- 📁 Automatic CSV export at session end

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

## 📐 Pupil Size Calibration (Optional)

Pupil coordinates are recorded in **pixels**, but researchers often need real-world units like **millimeters**.  
This app includes a **manual calibration function** to assist with that.

### 🔧 How it works:

1. Click the **Calibrate Pupil Size** button in the GUI.
2. The app captures a webcam image and displays it.
3. Click **two points** on an object with a known physical distance (e.g., 10 mm apart).
4. When prompted, enter the **real-world distance** (in mm).
5. The app computes and saves a **pixels-per-mm scale** to a file named `calibration.txt`.

✅ This calibration allows later conversion of pupil coordinates into **physical size units**,  
which is valuable for **pupillometry**, **behavioral science**, and **psychophysiological research**.


---

## 🤝 Contributing

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

