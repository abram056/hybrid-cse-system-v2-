from fastapi import FastAPI
from pydantic import BaseModel, Field
import numpy as np
from scipy.sparse import hstack, csr_matrix
import joblib

from hybrid_cse_system_v2.rbs.extractor import extract_rbs_features
from hybrid_cse_system_v2.interpreter.rbs_interpreter import generate_reasons


app = FastAPI()


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AnalysisResponse(BaseModel):
    prediction: str
    score: float
    reasons: list[str]


def combine_features(rbs_flags, tfidf_vector):
    rbs_array = np.array([list(rbs_flags.values())])
    rbs_sparse = csr_matrix(rbs_array)
    combined = hstack([tfidf_vector, rbs_sparse])
    return combined


def classify_text(text):
    labels = ["ham", "spam", "smish"]
    rbs_features = extract_rbs_features(text)
    tfidf_vector = tfidf_vectorizer.transform([text])
    combined_data = combine_features(rbs_features, tfidf_vector)
    label = model.predict(combined_data)[0]
    pred_probs = model.predict_proba(combined_data)[0]
    reasons = generate_reasons(rbs_features)

    return {
        "prediction": labels[label],
        "score": float(pred_probs[label]),
        "reasons": reasons,
    }


@app.on_event("startup")
def load_resources():
    global model, tfidf_vectorizer
    model = joblib.load("../../../models/mnb_model.joblib")
    tfidf_vectorizer = joblib.load("../../../models/tfidf_vectorizer.joblib")


@app.get("/")
def hello():
    return {"message": "CSE Detection API running.."}


@app.post("/analyse", response_model=AnalysisResponse)
def analyse(request: TextRequest):
    return classify_text(request.text)


@app.get("/health")
def health():
    try:
        assert model is not None
        assert tfidf_vectorizer is not None
        return {"status": "okay"}
    except Exception as e:
        return {"status": f"Error: {e}"}
