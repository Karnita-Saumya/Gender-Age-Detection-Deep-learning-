Setup
-----

1. Activate the existing virtual environment (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Or for Command Prompt:

```cmd
venv\Scripts\activate.bat
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Run (local)
---

- To run the web UI locally (serves a simple frontend and API):

```powershell
python server.py
```

- Open http://localhost:5000 in your browser and upload an image.

Docker (recommended for deployment)
---

Build and run the container locally:

```bash
docker build -t gad-app .
docker run -p 5000:5000 gad-app
```

Deployment notes
---

- This repository uses OpenCV and the provided model files (`*.caffemodel`, `*.pb`, `*.prototxt`). Those model files are large and include native dependencies. Vercel's Serverless Python environment is not well-suited for heavy native binaries like OpenCV and large model files.
- Recommended deployment targets: any container-friendly host (Render, Railway, Fly.io, DigitalOcean App Platform, AWS ECS) — they accept the `Dockerfile` included.
- If you must use Vercel, consider one of these approaches:
	- Host the inference service (this repo) on a container-friendly provider and use Vercel only for the static frontend which calls that API.
	- Reimplement inference with a pure JavaScript/TFJS model that runs in the browser (non-trivial and requires model conversion).

Files added for deployment
---

- `server.py`: Flask API that exposes `/predict` and serves a simple UI at `/`.
- `templates/index.html` and `static/style.css`: small interactive frontend.
- `Dockerfile` and `.dockerignore`: containerize the app for deployment.

Next steps
---

- Tell me where you'd like to deploy (Vercel / Render / Railway / other) and I will adapt the deployment instructions and help you set it up.
- I can also add a GitHub Actions workflow to build and push a Docker image to a registry and deploy automatically.
