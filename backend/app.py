import os
import sys
import pickle
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator

from utils import preprocess_text

# Configuration
MAX_TEXT_LENGTH = 1000
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.pkl")

# ---------------------------------------------------------------------------
# Load model pipeline at startup
# ---------------------------------------------------------------------------
def load_model():
    if not os.path.exists(MODEL_PATH):
        sys.stderr.write(
            "\nSTARTUP ERROR: Model file not found.\n"
            f"Expected: {MODEL_PATH}\n"
            "Please run 'python train_model.py' first.\n\n"
        )
        raise RuntimeError("Model file not found.")

    with open(MODEL_PATH, "rb") as f:
        pipeline = pickle.load(f)
    return pipeline

model_pipeline = load_model()

# ---------------------------------------------------------------------------
# FastAPI app setup
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Sentiment Analysis API",
    description="TF-IDF + Logistic Regression sentiment classifier.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / response models (DO NOT CHANGE - Frontend depends on these)
# ---------------------------------------------------------------------------
class PredictionRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if value is None or value.strip() == "":
            raise ValueError("Text field cannot be empty or whitespace-only.")
        if len(value) > MAX_TEXT_LENGTH:
            raise ValueError(f"Text field exceeds maximum length of {MAX_TEXT_LENGTH} characters.")
        return value

class PredictionResponse(BaseModel):
    sentiment: str
    confidence: float

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/")
def read_root():
    return {"message": "Sentiment Analysis API is running. Visit /docs for Swagger UI."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/predict", response_model=PredictionResponse)
def predict_sentiment(request: PredictionRequest):
    try:
        # 1. Clean the text
        cleaned_text = preprocess_text(request.text)

        if not cleaned_text:
            raise HTTPException(
                status_code=400,
                detail="Input text contains no usable words after cleaning."
            )

        # 2. Predict using the pickled Pipeline (handles TF-IDF internally)
        prediction = model_pipeline.predict([cleaned_text])[0]
        probabilities = model_pipeline.predict_proba([cleaned_text])[0]

        # 3. Get confidence score
        classes = list(model_pipeline.classes_)
        class_index = classes.index(prediction)
        confidence = float(probabilities[class_index])

        # 4. Return response matching frontend expectations
        return PredictionResponse(
            sentiment=prediction,
            confidence=round(confidence, 4),
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Could not process input: {e}")