Markdown
# ✋ Gesture-Controlled Distributed Robot System
### A Multi-Disciplinary Project: Computer Vision + Fuzzy Logic + PDC
This project demonstrates a real-time system where hand gestures are used to control the speed of multiple distributed robots. It was developed to fulfill the requirements for **6th Semester Parallel and Distributed Computing (PDC)** lab.
---
## 🌟 Features
*   **Computer Vision (CV):** Uses MediaPipe for high-performance hand landmark tracking.
*   **Fuzzy Logic Inference:** Implements human-like reasoning to ensure smooth speed transitions (e.g., Small distance = Slow speed).
*   **PDC & Distribution:** Utilizes Python's `multiprocessing` to simulate independent robot nodes receiving data in parallel.
---
## 🧠 System Architecture
### 1. The Perception (Computer Vision)
The system tracks the distance between the **Thumb Tip (ID 4)** and **Index Finger Tip (ID 8)**. This distance is calculated using the **Euclidean Distance** formula:
$$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
### 2. The Intelligence (Fuzzy Logic)
Instead of rigid "On/Off" logic, we use **Membership Functions**. If the distance is between categories (e.g., halfway between small and large), the system calculates a smooth, intermediate speed.
*   **Antecedent (Input):** Finger Distance (0 - 200 pixels)
*   **Consequent (Output):** Robot Speed (0 - 100%)
### 3. Execution (Parallel & Distributed Computing)
The project creates a **Master-Worker** architecture:
*   **Master Process:** Handles the Camera feed and Fuzzy calculations.
*   **Worker Processes:** Independent processes representing separate "Robots."
*   **Queue System:** A shared `multiprocessing.Queue` is used for **Message Passing**, ensuring all robots receive the speed command simultaneously without blocking the main video thread.
---
## 🛠️ Installation & Setup
### Prerequisites
*   **Anaconda** or **Miniconda** (Recommended)
*   **Python 3.11** (Critical for MediaPipe stability on Windows)
### 1. Create a Dedicated Environment
Open your terminal or Conda Prompt and run:
```bash
conda create -n gesture_env python=3.11
conda activate gesture_env
2. Install Required Libraries
Install the specific versions for maximum stability:
Bash
# Core CV and AI Libraries
pip install mediapipe==0.10.14
pip install opencv-python
# Logic and Math Libraries
pip install scikit-fuzzy
pip install scipy
pip install numpy
🚀 How to Run
Activate the environment:
Bash
conda activate gesture_env
Run the script:
Bash
python project.py
3.  **Interaction:**
    *   Bring your hand in front of the camera.
    *   **Pinch** your fingers to slow down the robots.
    *   **Spread** your fingers to increase the speed.
    *   Check the **Terminal** to see real-time speed data being received by **Robot 1** and **Robot 2**.
    *   Press **'ESC'** to close the program safely.
---
## 📂 Project Structure
```text
├── project.py          # Main source code
├── README.md           # Documentation
└── (env)               # Conda Virtual Environment
 