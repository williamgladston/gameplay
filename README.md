# 🚗 Gesture-Controlled Key Press Simulator for Hill Climb Racing

This project allows you to simulate key presses (`A` and `D`) programmatically using Python's `ctypes` library on Windows. It can be paired with hand gesture recognition (via MediaPipe) for hands-free control in games like **Hill Climb Racing**.

---

## 🎮 Features

- Simulate key presses using `ctypes.windll.user32.SendInput`
- Send virtual key codes for `A` (Brake) and `D` (Gas)
- Compatible with gesture input from camera (via MediaPipe)
- Designed specifically for games that require real-time input like *Hill Climb Racing*

---

## 🧰 Requirements

- Python 3.x
- Windows OS
- (Optional) Webcam and `mediapipe` for gesture control

### Python Libraries

If using gestures:
```bash

pip install opencv-python mediapipe pynput

🚀 Usage
	1.	Basic Auto Press Simulation
python keypress_simulator.py
It will alternate between pressing and releasing A and D every 0.5 seconds.
	2.	Integrate with Gesture Control

Use the script with MediaPipe hand detection:
	•	Show ✊ (fist) → Press A
	•	Show 🖐️ (open palm) → Press D
💻 Code Structure
	•	keypress_simulator.py - Main file to simulate A and D key presses
	•	gesture_control.py (optional) - Uses MediaPipe to map gestures to key presses
⚠️ Disclaimer

This project simulates keyboard input. Use responsibly and do not use for automating actions in online games or violating game terms of service.
