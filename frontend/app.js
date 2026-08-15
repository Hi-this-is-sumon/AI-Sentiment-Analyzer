const API_URL = "https://sentiment-api-backend-1ml0.onrender.com";
const API_URL = "http://127.0.0.1:8000";

const textarea = document.getElementById("sentence-input");
const charCount = document.getElementById("char-count");
const predictBtn = document.getElementById("predict-btn");
const btnText = document.getElementById("btn-text");
const btnSpinner = document.getElementById("btn-spinner");
const errorBox = document.getElementById("error-box");
const resultBox = document.getElementById("result-box");
const resultLabel = document.getElementById("result-label");
const resultConfidence = document.getElementById("result-confidence");
const confidenceBarFill = document.getElementById("confidence-bar-fill");

// --- Character counter ---
textarea.addEventListener("input", () => {
  charCount.textContent = textarea.value.length;
});

// --- Helpers ---
function showError(message) {
  errorBox.textContent = message;
  errorBox.classList.remove("hidden");
}

function hideError() {
  errorBox.classList.add("hidden");
  errorBox.textContent = "";
}

function hideResult() {
  resultBox.classList.add("hidden");
  resultBox.classList.remove("positive", "negative");
}

function showResult(sentiment, confidence) {
  const percent = Math.round(confidence * 100);

  resultLabel.textContent = sentiment.toUpperCase();
  resultConfidence.textContent = `Confidence: ${percent}%`;
  confidenceBarFill.style.width = `${percent}%`;

  resultBox.classList.remove("hidden", "positive", "negative");
  resultBox.classList.add(sentiment.toLowerCase() === "positive" ? "positive" : "negative");
}

function setLoading(isLoading) {
  predictBtn.disabled = isLoading;
  btnText.textContent = isLoading ? "Analyzing..." : "Predict Sentiment";
  btnSpinner.classList.toggle("hidden", !isLoading);
}

// --- Main predict handler ---
async function handlePredict() {
  const text = textarea.value.trim();

  hideError();
  hideResult();

  if (text === "") {
    showError("Please enter a sentence before predicting.");
    return;
  }

  setLoading(true);

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text: text }),
    });

    if (!response.ok) {
      // Try to read the API's error detail, otherwise fall back to a
      // generic message.
      let detail = "Something went wrong while analyzing your text.";
      try {
        const errorData = await response.json();
        if (errorData && errorData.detail) {
          detail =
            typeof errorData.detail === "string"
              ? errorData.detail
              : JSON.stringify(errorData.detail);
        }
      } catch (_) {
        // response body wasn't valid JSON; keep the generic message
      }
      showError(detail);
      return;
    }

    const data = await response.json();
    showResult(data.sentiment, data.confidence);
  } catch (err) {
    // Network error: backend not running, wrong port, CORS issue, etc.
    showError(
      "Could not reach the backend. Is it running at " +
        API_URL +
        "? (Check that uvicorn is started and CORS is configured.)"
    );
  } finally {
    setLoading(false);
  }
}

predictBtn.addEventListener("click", handlePredict);

// Allow Ctrl+Enter / Cmd+Enter to submit from the textarea.
textarea.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "Enter") {
    handlePredict();
  }
});
