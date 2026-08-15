# 🧠 AI Sentiment Analyzer — Full-Stack ML Project
# AI Sentiment Analyzer

Live demo: https://ai-sentiment-analyzer-ochre.vercel.app/

Small, easy-to-run full-stack sentiment analysis application.

- **Frontend:** Vanilla HTML/CSS/JS (static app served on Vercel)
- **Backend:** FastAPI (TF-IDF + Logistic Regression pipeline)
- **Model:** Trained locally with provided scripts and saved to `backend/models/sentiment_model.pkl`

This README contains quick start instructions, deployment notes, API documentation, and contributor guidance.

---

## Project layout

```text
sentiment-analysis-app/
├── backend/           # FastAPI app, training script, model, dataset
├── frontend/          # Static frontend (index.html, style.css, app.js)
├── LICENSE
└── README.md
```

## Live demo

View the running frontend here:

https://ai-sentiment-analyzer-ochre.vercel.app/

The frontend talks to the deployed backend at:

https://sentiment-api-backend-1ml0.onrender.com/

---

## Quick start (local development)

Prerequisites

- Python 3.10+ and pip
- Node.js (optional if you only open `frontend/index.html` locally)

Run backend locally

1. Create and activate a Python virtual environment (recommended):

```bash
cd backend
python -m venv .venv
source .venv/bin/activate    # macOS / Linux
.venv\Scripts\Activate.ps1  # Windows PowerShell
```

2. Install dependencies and train the model (first-time only):

```bash
pip install -r requirements.txt
python train_model.py
```

3. Start the API server:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

Open the frontend locally

- Open `frontend/index.html` in a browser or serve the `frontend/` folder (for example with `npx http-server` or `python -m http.server 8000`).
- When the page is loaded from `localhost`, the frontend will call the local backend at `http://127.0.0.1:8000`.

---

## API (HTTP)

Base URL (production):

```
https://sentiment-api-backend-1ml0.onrender.com
```

Endpoints

- `GET /` — basic root health message
- `GET /health` — health check returning `{ "status": "healthy" }`
- `POST /predict` — analyze text. Request JSON:

```json
{ "text": "your sentence here" }
```

Response JSON:

```json
{ "sentiment": "Positive|Negative", "confidence": 0.9123 }
```

---

## Deployment notes

- Frontend is deployed on Vercel. The repository includes `vercel.json` to serve the `frontend/` folder as a static site.
- Backend is deployed on Render and is available at `https://sentiment-api-backend-1ml0.onrender.com/`.

If you redeploy the frontend or move the backend, update the frontend `API_URL` accordingly (the app detects `localhost` and will use the local API automatically when developing).

CORS: The backend currently allows requests from any origin. For stricter security, update `backend/app.py` and configure `allow_origins` to your frontend domain.

---

## Contributing

Contributions are welcome. Typical workflows:

1. Fork the repo and create a feature branch
2. Make changes and run the backend/frontend locally
3. Open a pull request with a clear description of changes

Please ensure model changes are reproducible by including training commands if you update `train_model.py`.

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ by Sumon Mandal

> **IBM Industrial Training Project** | Developed by **Sumon**

A complete Sentiment Analysis web application that classifies text as **Positive** or **Negative**. This project leverages a custom-built **TF-IDF + Logistic Regression pipeline** trained on a balanced dataset of 3,000 real-world reviews, served through a high-speed FastAPI backend and an interactive Vanilla HTML/CSS/JS frontend.

---

## 1. Project Structure

```text
sentiment-analysis-app/
│
├── backend/
│   ├── app.py              # FastAPI server: loads the saved model, exposes /predict
│   ├── train_model.py      # Run once: parses data, trains pipeline + saves model
│   ├── utils.py             # Shared text preprocessing (used by both files above)
│   ├── requirements.txt    # Project dependencies
│   ├── data/               # Contains the raw CSV/TXT datasets (Amazon, IMDb, Yelp)
│   └── models/               # Created automatically by train_model.py
│       ├── sentiment_model.pkl    # The combined TF-IDF + Classifier pipeline
│       └── confusion_matrix.png   # Visual evaluation report
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── LICENSE                 # MIT License file
└── README.md               # Project documentation

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.