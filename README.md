# 🤖 AI Navigation System for Visually Impaired

An AI-powered navigation system designed to assist visually impaired users by detecting nearby objects in real time using **YOLOv8** and **OpenCV**. The system provides voice guidance, secure user authentication, and a Flask-based dashboard for an enhanced user experience.

---

## 📌 Features

- 🔐 User Registration and Login
- 🔒 Secure Password Hashing
- 💾 SQLite Database Integration
- 🤖 Real-Time Object Detection using YOLOv8
- 📷 Live Camera-Based Navigation
- 🔊 Voice Guidance for Detected Objects
- 📍 Object Direction Detection (Left, Right, Ahead)
- 📏 Distance Estimation (Far, Medium, Close, Very Close)
- 📜 Detection History Logging
- 📊 Flask Dashboard
- 🎨 Responsive User Interface using HTML, CSS, and JavaScript

---

## 🛠️ Technologies Used

- Python
- Flask
- YOLOv8
- OpenCV
- SQLite
- HTML5
- CSS3
- JavaScript
- Werkzeug
- pywin32

---

## 📂 Project Structure

```
AI_NAVIGATION_SYSTEM/
│
├── app.py
├── navigation.py
├── database.py
├── users.db
├── detections.txt
├── requirements.txt
├── README.md
├── yolov8n.pt
│
├── static/
│   └── style.css
│
└── templates/
    ├── home.html
    ├── login.html
    ├── register.html
    └── dashboard.html
```

---

## 🚀 Installation

### 1. Clone the repository

```bash
git clone https://github.com/sharanyasureshs12/AI-Navigation-System.git
```

### 2. Navigate to the project folder

```bash
cd AI-Navigation-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python app.py
```

### 5. Open in your browser

```
http://127.0.0.1:5000
```

---

## 🎯 How It Works

1. Register a new account or log in.
2. Access the dashboard.
3. Click **Start Navigation**.
4. The webcam starts capturing live video.
5. YOLOv8 detects nearby objects.
6. The system identifies object direction and estimated distance.
7. Voice guidance alerts the user about detected obstacles.
8. Detection history is stored for future reference.



## 📈 Future Enhancements

- Live camera feed inside the dashboard
- Mobile application support
- GPS-based navigation
- Multi-language voice guidance
- Cloud database integration
- Email verification
- Detection analytics and reports

---

## 👩‍💻 Author

**Sharanya Suresh**

- GitHub: https://github.com/sharanyasureshs12
- LinkedIn: https://www.linkedin.com/in/sharanya-suresh-58b1a926a

---

## ⭐ If you like this project

Please consider giving it a ⭐ on GitHub!
