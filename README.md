# Task 11 - Full Application Containerization

## Objective
Containerize the complete MNIST deep learning solution: trained model, Flask API, and Streamlit UI.

## Architecture
Two Docker Compose services work together:

- flask-api: loads deep_learning_model.h5 and exposes /, /health and /predict on port 5000.
- streamlit-ui: provides the browser interface on port 8501 and calls http://flask-api:5000 inside the Compose network.

```text
Browser -> Streamlit UI :8501 -> Flask API :5000 -> deep_learning_model.h5
                         <- JSON prediction <-
```

## Run
```powershell
docker compose build
docker compose up -d
docker compose ps
```

Open http://localhost:8501

## Validation
The local Task 11 run demonstrated successful image builds, healthy Compose services, model loading, Streamlit prediction, Flask JSON prediction, automated API validation, Docker resource inspection, logs, and container-to-container health communication.

Observed sample: 7.png was predicted as digit 7 with 99.99% confidence.

## Optimization
- Python 3.12 slim images
- Multi-stage API build
- pip --no-cache-dir
- .dockerignore
- Non-root runtime users
- Docker health checks
- Gunicorn for Flask
- Dedicated Compose bridge network
- FLASK_API_URL environment variable

## Required model
Copy the compatible trained model to api/deep_learning_model.h5 before building.

## Evidence
See screenshots/README.md and report/ for the final evidence checklist and deployment report.

Author: Saikumar Padala
Course: MSc Artificial Intelligence