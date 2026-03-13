from hybrid_cse_system_v2.api.app import MLModels


def setup_module():
    """
    Runs once before all tests in this file.
    Loads the real model and vectorizer for the pipeline.
    """
    global models

    models = MLModels(
        "models/mnb_model.joblib",
        "models/tfidf_vectorizer.joblib"
    )


def test_pipeline_returns_valid_structure():
    text = "Hello, are we still meeting after class?"

    result = models.predict(text)

    assert isinstance(result, dict)

    assert "prediction" in result
    assert "score" in result
    assert "reasons" in result

    assert result["prediction"] in ["ham", "spam", "smish"]
    assert isinstance(result["score"], float)
    assert isinstance(result["reasons"], list)


def test_smishing_message_generates_reasons():
    text = "Urgent! Verify your account immediately https://fakebank.xyz"

    result = models.predict(text)

    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) > 0


def test_ham_message_generates_no_reasons():
    text = "Hey bro, are you coming to class today?"

    result = models.predict(text)

    assert isinstance(result["reasons"], list)
    assert len(result["reasons"]) == 0


def test_pipeline_handles_url_features():
    text = "Claim your free prize now https://freegift.xyz"

    result = models.predict(text)

    assert isinstance(result["prediction"], str)
    assert 0.0 <= result["score"] <= 1.0


def test_pipeline_handles_long_text():
    text = (
        "Dear customer, we detected suspicious activity on your account. "
        "Please verify immediately to avoid suspension. "
        "Click the secure link below to confirm your details "
        "https://secure-check.xyz immediately."
    )

    result = models.predict(text)

    assert isinstance(result["prediction"], str)
    assert isinstance(result["score"], float)
