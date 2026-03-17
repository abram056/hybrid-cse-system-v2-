from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, Request
from pydantic import BaseModel, Field
import numpy as np
from scipy.sparse import hstack, csr_matrix
import joblib
from typing import Any
from pathlib import Path

from hybrid_cse_system_v2.rbs.extractor import extract_rbs_features
from hybrid_cse_system_v2.interpreter.rbs_interpreter import generate_reasons


BASE_DIR = Path(__file__).resolve().parents[3]

MODEL_PATH = BASE_DIR / "models" / "mnb_model.joblib"
VECTORIZER_PATH = BASE_DIR / "models" / "tfidf_vectorizer.joblib"


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class AnalysisResponse(BaseModel):
    prediction: str
    score: float
    reasons: list[str]


class MLModels:
    def __init__(self, model_path: str, vectorizer_path: str):
        self.model = joblib.load(model_path)
        self.tfidf_vectorizer = joblib.load(vectorizer_path)

    def predict(self, text: str):
        labels = ["ham", "spam", "smish"]
        rbs_features = extract_rbs_features(text)
        tfidf_vector = self.tfidf_vectorizer.transform([text])
        combined_data = self._combine_features(rbs_features, tfidf_vector)
        label = self.model.predict(combined_data)[0]
        pred_probs = self.model.predict_proba(combined_data)[0]
        reasons = generate_reasons(rbs_features)

        return {
            "prediction": labels[label],
            "score": float(pred_probs[label]),
            "reasons": reasons,
        }

    def _combine_features(self, rbs_flags, tfidf_vector):
        rbs_array = np.array([list(rbs_flags.values())])
        rbs_sparse = csr_matrix(rbs_array)
        combined = hstack([tfidf_vector, rbs_sparse])
        return combined


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize models and attach to app.state
    app.state.ml_models = MLModels(
        str(MODEL_PATH.resolve()),
        str(VECTORIZER_PATH.resolve())
    )

    yield
    # Cleanup
    app.state.ml_models = None


app = FastAPI(lifespan=lifespan)


# Dependency to get ML models
def get_ml_models(request: Request) -> MLModels:
    return request.app.state.ml_models


@app.get("/")
def hello():
    return {"message": "CSE Detection API running.."}


@app.post("/analyse", response_model=AnalysisResponse)
def analyse(
    request: TextRequest,
    ml_models: MLModels = Depends(get_ml_models)
):
    return ml_models.predict(request.text)


@app.get("/health")
def health(ml_models: MLModels = Depends(get_ml_models)):
    try:
        assert ml_models is not None
        return {"status": "okay"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
