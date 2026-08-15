import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from utils import preprocess_text

# Configuration
BASE_DIR = os.path.dirname(__file__)
MODELS_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")

MODEL_PATH = os.path.join(MODELS_DIR, "sentiment_model.pkl")
CONFUSION_MATRIX_PATH = os.path.join(MODELS_DIR, "confusion_matrix.png")


def load_data_from_folder(data_dir: str) -> pd.DataFrame:
    """
    Unstoppable parser: Aggressively strips quotes, commas, and spaces 
    from the end of the line to expose the hidden 0 or 1 label.
    """
    records = []
    if not os.path.isdir(data_dir):
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")

    for fname in os.listdir(data_dir):
        if not fname.lower().endswith(('.csv', '.txt')):
            continue
        
        path = os.path.join(data_dir, fname)
        
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # 1. Strip all whitespace, newlines, quotes, and commas from the VERY END
                cleaned_line = line.rstrip(' \r\n\t"\',')
                if not cleaned_line:
                    continue
                
                # 2. Now the absolute last character should safely be the 0 or 1
                if cleaned_line[-1] in ('0', '1'):
                    label = int(cleaned_line[-1])
                    
                    # 3. Grab the text (everything before the label)
                    text_part = cleaned_line[:-1]
                    
                    # 4. Clean up any trailing/leading delimiters from the text itself
                    text = text_part.strip(' \t,;"\'')
                    
                    if text:
                        records.append({'text': text, 'label_raw': label})

    if not records:
        raise ValueError("No valid data could be parsed from the data directory.")

    df = pd.DataFrame(records)
    
    # Map to sentiment strings
    df['sentiment'] = df['label_raw'].map({1: 'Positive', 0: 'Negative'})
    
    # Shuffle the dataset
    df = df[['text', 'sentiment']].sample(frac=1, random_state=42).reset_index(drop=True)
    return df


def validate_dataset(df: pd.DataFrame):
    print("=" * 60)
    print("DATASET SUMMARY")
    print("=" * 60)
    print(f"Total rows: {len(df)}")
    print(f"\nClass distribution:\n{df['sentiment'].value_counts()}")
    print("=" * 60)


def main():
    os.makedirs(MODELS_DIR, exist_ok=True)

    # 1. Load Data
    print(f"Loading data from {DATA_DIR}...")
    df = load_data_from_folder(DATA_DIR)
    validate_dataset(df)
    
    # 2. Preprocess text
    print("Preprocessing text...")
    df["cleaned_text"] = df["text"].apply(preprocess_text)
    df = df[df["cleaned_text"].str.len() > 0] # Remove empty texts

    # 3. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        df["cleaned_text"],
        df["sentiment"],
        test_size=0.2,
        random_state=42,
        stratify=df["sentiment"],
    )

    # 4. Create and Train Pipeline (Vectorizer + Classifier)
    print("\nTraining TF-IDF + Logistic Regression Pipeline...")
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=5000)),
        ('clf', LogisticRegression(C=2.0, class_weight='balanced', random_state=42, max_iter=1000))
    ])
    
    pipeline.fit(X_train, y_train)

    # 5. Evaluate Model
    y_pred = pipeline.predict(X_test)
    print("\n" + "=" * 60)
    print("EVALUATION RESULTS")
    print("=" * 60)
    print(f"Accuracy:  {accuracy_score(y_test, y_pred):.4f}")
    print(f"Precision: {precision_score(y_test, y_pred, pos_label='Positive', zero_division=0):.4f}")
    print(f"Recall:    {recall_score(y_test, y_pred, pos_label='Positive', zero_division=0):.4f}")
    print(f"F1-score:  {f1_score(y_test, y_pred, pos_label='Positive', zero_division=0):.4f}")
    print("\nClassification Report:\n", classification_report(y_test, y_pred, zero_division=0))

    # 6. Save Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=["Positive", "Negative"])
    try:
        plt.figure(figsize=(5, 4))
        sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", 
                    xticklabels=["Positive", "Negative"], 
                    yticklabels=["Positive", "Negative"])
        plt.xlabel("Predicted")
        plt.ylabel("Actual")
        plt.title("Confusion Matrix")
        plt.tight_layout()
        plt.savefig(CONFUSION_MATRIX_PATH)
        plt.close()
    except Exception as e:
        pass

    # 7. Save Model as a single Pickle file
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(pipeline, f)

    print("\nTraining completed successfully. Model saved as sentiment_model.pkl in /models.")

if __name__ == "__main__":
    main()