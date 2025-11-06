KaunHaiBe!

“Ab har nazar pe nazar hai”

📘 Overview

KaunHaiBe! is a privacy-focused Python desktop app that uses your webcam and AI (MediaPipe + OpenCV) to detect when someone looks at your screen from behind.
If a sustained gaze is detected for 5 seconds, it shows a funny popup alert letting you dismiss or minimize your windows instantly.

⚙️ Tech Stack

Python 3.8+ – Base language

OpenCV – Webcam access & frame handling

MediaPipe – FaceMesh & iris landmark detection

NumPy – Gaze direction and math operations

Tkinter – GUI & popup alerts

PyAutoGUI – Window minimize automation

Threading – Real-time background monitoring

🧠 Core Features

Detects up to 5 faces at once

Tracks eye gaze direction using iris landmarks

Alerts only after 5 seconds of sustained peeking

100% local processing — no data saved or sent

Runs smoothly at ~20 FPS