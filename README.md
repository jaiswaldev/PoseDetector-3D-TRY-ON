# 🧍‍♂️ Real-Time Pose Detection Web App

A full-stack web application for **real-time human pose detection** using **OpenCV + MediaPipe**, built with a **React (Vite)** frontend and a **FastAPI** backend. Live webcam feed is streamed using **MJPEG**, enabling fast and responsive pose tracking in the browser.

## 💻 GitHub Repo
👉 [GitHub Repository](https://github.com/jaiswaldev/PoseDetector-3D-TRY-ON)

---

## 🛠 Tech Stack

- **Frontend**: React (Vite), HTML5, TailwindCSS
- **Backend**: FastAPI, Python
- **Computer Vision**: OpenCV, MediaPipe
- **Streaming**: MJPEG over HTTP

---

## 🎯 Features

- Real-time pose detection with 33 human body landmarks
- MJPEG video streaming with <100ms latency
- 15–25 FPS performance on standard consumer hardware
- Modular API design for scaling to multi-user or activity recognition
- Responsive and lightweight UI built with React + Vite

---

## 📦 Installation & Setup

### 🔹 Backend (FastAPI + OpenCV + MediaPipe)
```bash
git clone https://github.com/jaiswaldev/PoseDetector-3D-TRY-ON.git
cd PoseDetector-3D-TRY-ON/backend
pip install -r requirements.txt
uvicorn main:app --reload


🔹 Frontend (React + Vite)
```bash
cd ../frontend
npm install
npm run dev


##
**Make sure the backend is running before starting the frontend.**

