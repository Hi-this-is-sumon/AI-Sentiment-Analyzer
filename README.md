```markdown
# 🧠 AI Sentiment Analyzer — Full-Stack ML Project

> **IBM Industrial Training Project** | Developed by **Sumon Mandal**

A full-stack sentiment analysis web application that classifies text as **Positive** or **Negative** in real time. This project leverages a custom-built **TF-IDF + Logistic Regression pipeline** trained on a balanced dataset of 3,000 real-world reviews, served through a high-speed FastAPI backend and an interactive Vanilla HTML/CSS/JS frontend.

---

## 🌐 Live Demo

*   **Frontend (Vercel):** [https://ai-sentiment-analyzer-ochre.vercel.app/](https://ai-sentiment-analyzer-ochre.vercel.app/)
*   **Backend API (Render):** [https://sentiment-api-backend-1ml0.onrender.com/](https://sentiment-api-backend-1ml0.onrender.com/)
*   **Interactive Swagger API Docs:** [https://sentiment-api-backend-1ml0.onrender.com/docs](https://sentiment-api-backend-1ml0.onrender.com/docs)

---

## 📁 1. Project Structure

```text
sentiment-analysis-app/
│
├── backend/
│   ├── app.py              # FastAPI server: loads model, exposes /predict
│   ├── train_model.py      # Data parser, pipeline training & model exporter
│   ├── utils.py            # Shared text preprocessing logic
│   ├── requirements.txt    # Python dependencies
│   ├── data/               # Raw CSV datasets (Amazon, IMDb, Yelp)
│   └── models/             # Auto-generated model artifacts
│       ├── sentiment_model.pkl    # Serialized TF-IDF + Logistic Regression pipeline
│       └── confusion_matrix.png   # Confusion matrix evaluation plot
│
├── frontend/
│   ├── index.html          # Application UI
│   ├── style.css           # Styling & animations
│   └── app.js              # API integration & dynamic DOM rendering
│
├── LICENSE                 # MIT License
├── vercel.json             # Vercel config for serving `frontend/`
└── README.md               # Project documentation
```

## 📊 2. Model & Dataset Summary

- **Dataset:** 3,000 balanced real-world reviews (1,500 Positive, 1,500 Negative) aggregated from Amazon, IMDb, and Yelp.
- **Preprocessing:** Custom whitespace collapsing, lowercase conversion, and punctuation stripping.
- **Feature Extraction:** TF-IDF Vectorizer with unigram and bigram ranges (`ngram_range=(1, 2)`).
- **Classification:** Logistic Regression with balanced class weights.
- **Performance:**

- **Accuracy:** ~81.00%
- **Precision:** ~79.81%
- **Recall:** ~83.00%
- **F1-Score:** ~81.37%

## 🚀 3. Quick Start (Local Development)

### Prerequisites

- Python 3.10+
- pip

### Step 1: Clone the Repository
Bash

```
git clone https://github.com/Hi-this-is-sumon/AI-Sentiment-Analyzer.git
cd AI-Sentiment-Analyzer
```

### Step 2: Backend Setup
Bash

```
cd backend
python -m venv .venv
```

**Activate the virtual environment:**

- **Windows (PowerShell):** `.venv\Scripts\Activate.ps1`
- **Windows (CMD):** `.venv\Scripts\activate.bat`
- **macOS / Linux:** `source .venv/bin/activate`
**Install dependencies & train model:**

Bash

```
pip install -r requirements.txt
python train_model.py
```

**Start the FastAPI server:**

Bash

```
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

The API will be live at `http://127.0.0.1:8000`.

### Step 3: Frontend Setup
Open `frontend/index.html` using the **VS Code Live Server** extension or run a local HTTP server:

Bash

```
cd ../frontend
python -m http.server 5500
```

Visit `http://127.0.0.1:5500` in your browser.

## 🔌 4. API Documentation

### Base URL

- **Local:** `http://127.0.0.1:8000`
- **Production:** `https://sentiment-api-backend-1ml0.onrender.com`

### Endpoints

#### 1. Root Status

- **Method:** `GET /`
- **Response:**

JSON

```
{
	"message": "Sentiment Analysis API is running. Visit /docs for Swagger UI."
}
```

#### 2. Health Check

- **Method:** `GET /health`
- **Response:**

JSON

```
{
	"status": "healthy"
}
```

#### 3. Predict Sentiment

- **Method:** `POST /predict`
- **Headers:** `Content-Type: application/json`
- **Request Body:**

JSON

```
{
	"text": "The camera takes stunning, crisp photos in low light."
}
```
- **Response Body:**

JSON

```
{
	"sentiment": "Positive",
	"confidence": 0.9452
}
```

## ☁️ 5. Deployment Architecture

- **Frontend:** Hosted on **Vercel** as a static site mapped to the `frontend/` root directory.
- **Backend:** Hosted on **Render** as a Python Web Service with:

- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app:app --host 0.0.0.0 --port $PORT`

## 📜 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

Made with ❤️ by **Sumon Mandal**
