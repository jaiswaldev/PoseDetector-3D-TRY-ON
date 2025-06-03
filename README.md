# 🧍‍♂️ Real-Time Pose Detection Web App

A full-stack web application for **real-time human pose detection** using **OpenCV + MediaPipe**, built with a **React (Vite)** frontend and a **FastAPI** backend. The webcam feed is streamed via **MJPEG**, enabling fast and responsive pose tracking directly in the browser.

---

## 💻 GitHub Repository

👉 [PoseDetector-3D-TRY-ON](https://github.com/jaiswaldev/PoseDetector-3D-TRY-ON)

---

## 🛠️ Tech Stack

- **Frontend**: React (Vite), HTML5, Tailwind CSS  
- **Backend**: FastAPI, Python  
- **Computer Vision**: OpenCV, MediaPipe  
- **Streaming**: MJPEG over HTTP

---

## 🎯 Features

- ✅ Real-time pose detection with **33 human body landmarks**
- 🚀 **MJPEG video streaming** with sub-100ms latency
- 🎥 Smooth performance: **15–25 FPS** on standard consumer hardware
- ⚙️ **Modular API** design — ready for multi-user support or activity recognition
- 📱 Lightweight, responsive UI built with **React + TailwindCSS**

---

## 📦 Installation & Setup

### 🔹 Backend (FastAPI + OpenCV + MediaPipe)

```bash
# Clone the repository
git clone https://github.com/jaiswaldev/PoseDetector-3D-TRY-ON.git

# Navigate to backend
cd PoseDetector-3D-TRY-ON/backend

# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI backend
uvicorn main:app --reload
```

---

### 🔹 Frontend (React + Vite)

```bash
# Navigate to frontend
cd ../frontend

# Install frontend dependencies
npm install

# Start the Vite dev server
npm run dev
```

> ⚠️ **Note:** Ensure the **backend is running first** before launching the frontend for smooth MJPEG video streaming.

---

## 🌟 What's Next

I'm working on extending this project into a **Virtual 3D Try-On System** for the fashion industry, where:

- 🧍 **Pose data** will be used to extract accurate body proportions
- 👕 Users will get **fit suggestions** based on brand-specific sizing data
- 🛍️ Customers can confidently purchase clothes online **without worrying about fitting issues**

Stay tuned for more updates and releases!

---