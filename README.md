# 🧠 AI Sentiment Analyzer — Full-Stack ML Project

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