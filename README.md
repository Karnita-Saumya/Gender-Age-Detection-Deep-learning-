<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=30&pause=1000&color=6C63FF&center=true&vCenter=true&width=600&lines=Gender+%26+Age+Detection;Powered+by+Deep+Learning;OpenCV+%2B+Flask+%2B+Docker" alt="Typing SVG" />

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Deep Learning](https://img.shields.io/badge/Deep_Learning-Caffe_Models-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white)

<br/>

> 🧠 **Real-time Gender & Age prediction** from facial images using pre-trained Caffe deep learning models wrapped in a clean Flask web interface.

</div>

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧑‍🤝‍🧑 **Gender Detection** | Classifies faces as Male or Female |
| 🎂 **Age Estimation** | Predicts age group from facial features |
| 🌐 **Web Interface** | Upload images via a simple browser UI |
| 🐳 **Docker Support** | One-command containerised deployment |
| ⚡ **REST API** | `/predict` endpoint for programmatic access |

---

## 🏗️ Project Structure

```
Gender-Age-Detection-Deep-learning/
│
├── 📁 static/
│   └── style.css              # Frontend styles
│
├── 📁 templates/
│   └── index.html             # Web UI template
│
├── 🐍 app.py                  # Core detection logic
├── 🐍 gad.py                  # Gender & age detection helpers
├── 🐍 server.py               # Flask server — exposes /predict
│
├── 🐳 Dockerfile              # Container definition
├── 🐳 .dockerignore
├── 📋 requirements.txt
├── 🙈 .gitignore
│
└── 🖼️ Sample images (girl2.jpg, man1.jpg, kid1.jpg …)
```

> **Note:** The pre-trained model files (`*.caffemodel`, `*.pb`, `*.prototxt`) must be present locally — they are not tracked by Git due to their size.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- The model weight files placed in the project root

### 1 · Clone the repo

```bash
git clone https://github.com/Karnita-Saumya/Gender-Age-Detection-Deep-learning-.git
cd Gender-Age-Detection-Deep-learning-
```

### 2 · Activate virtual environment

<details>
<summary>🪟 <strong>PowerShell (Windows)</strong></summary>

```powershell
.\venv\Scripts\Activate.ps1
```

</details>

<details>
<summary>💻 <strong>Command Prompt (Windows)</strong></summary>

```cmd
venv\Scripts\activate.bat
```

</details>

<details>
<summary>🐧 <strong>Linux / macOS</strong></summary>

```bash
source venv/bin/activate
```

</details>

### 3 · Install dependencies

```bash
pip install -r requirements.txt
```

### 4 · Run the app

```bash
python server.py
```

🌐 Open **http://localhost:5000** in your browser and upload any image!

---

## 🐳 Docker (Recommended for Deployment)

The cleanest way to run or ship this app — no environment headaches.

```bash
# Build the image
docker build -t gad-app .

# Run the container
docker run -p 5000:5000 gad-app
```

Then visit **http://localhost:5000** as usual.

---

## 🌍 Deployment Guide

### ✅ Recommended Platforms (Container-friendly)

| Platform | Notes |
|---|---|
| 🟢 **Render** | Free tier, auto-deploys from GitHub |
| 🚂 **Railway** | Simple push-to-deploy |
| ✈️ **Fly.io** | Global edge deployment |
| 🌊 **DigitalOcean App Platform** | Managed containers |
| ☁️ **AWS ECS / Fargate** | Production-grade, scalable |

All of the above accept the included `Dockerfile` directly.

### ⚠️ Vercel — Not Recommended (but possible workarounds)

Vercel's Serverless Python environment does **not** support heavy native binaries like OpenCV or large model files. If you must use Vercel, choose one of these approaches:

<details>
<summary><strong>Option A · Split Architecture</strong></summary>

Host the inference service (this repo) on Render/Railway/Fly.io and deploy only the static frontend on Vercel, pointing API calls to the external service URL.

</details>

<details>
<summary><strong>Option B · Browser-side Inference (advanced)</strong></summary>

Convert the model to TensorFlow.js format and run inference entirely in the browser — no backend required. This is non-trivial and requires model conversion tooling.

</details>

---

## 🔌 API Reference

### `POST /predict`

Upload an image and receive gender & age predictions.

```bash
curl -X POST http://localhost:5000/predict \
  -F "image=@path/to/photo.jpg"
```

**Response example:**
```json
{
  "gender": "Male",
  "age": "(25-32)"
}
```

---

## 🧬 How It Works

```
Input Image
     │
     ▼
┌─────────────────────┐
│  Face Detection     │  ← OpenCV DNN (Caffe)
│  (*.caffemodel)     │
└────────┬────────────┘
         │  Detected face ROI
         ▼
┌─────────────────────┐    ┌─────────────────────┐
│  Gender Net         │    │  Age Net            │
│  (*.prototxt +      │    │  (*.prototxt +      │
│   *.caffemodel)     │    │   *.caffemodel)     │
└────────┬────────────┘    └────────┬────────────┘
         │                          │
         └──────────┬───────────────┘
                    ▼
          { gender, age_range }
```

---

## 🛠️ Tech Stack

- **OpenCV** — face detection + DNN inference
- **Caffe pre-trained models** — gender & age classification
- **Flask** — lightweight Python web framework
- **Docker** — containerisation & portable deployment
- **HTML / CSS** — minimal interactive frontend

---

## 🗺️ Roadmap / Next Steps

- [ ] 🔄 Add GitHub Actions CI/CD workflow (auto-build & push Docker image)
- [ ] ☁️ One-click deploy to Render / Railway
- [ ] 📊 Add confidence scores to API response
- [ ] 🎥 Real-time webcam support
- [ ] 🖼️ Multi-face detection in a single image

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push and open a PR

---

## 📄 License

This project is open source. See the repository for details.

---

<div align="center">

Made with ❤️ by [Karnita-Saumya](https://github.com/Karnita-Saumya)

⭐ **Star this repo if you found it useful!**

</div>
