
import joblib
import pandas as pd

from src.feature_extractor import extract_features
from src.risk_scorer import calculate_risk


# Load the trained Random Forest model
model = joblib.load("models/phishing_model.pkl")


def predict_url(url):
    """Analyse a URL and return prediction and risk details."""

    # Step 1: Extract URL features
    features = extract_features(url)

    # Step 2: Convert features into a DataFrame
    input_data = pd.DataFrame([features])

    # Step 3: Get model prediction
    prediction = model.predict(input_data)[0]

    # Step 4: Get prediction probabilities
    probabilities = model.predict_proba(input_data)[0]

    # Step 5: Calculate phishing probability
    phishing_probability = probabilities[
        list(model.classes_).index(1)
    ] * 100

    # Step 6: Generate prediction label
    if prediction == 1:
        result = "Potentially Phishing"
    else:
        result = "Likely Legitimate"

    # Step 7: Calculate risk score
    risk = calculate_risk(
        features,
        phishing_probability
    )

    # Step 8: Return complete analysis
    return {
        "url": url,
        "prediction": result,
        "phishing_probability": round(
            phishing_probability, 2
        ),
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "reasons": risk["reasons"],
        "features": features
    }


if __name__ == "__main__":

    test_url = "https://example.com"

    result = predict_url(test_url)

    print("\n========== PhishSentinel Analysis ==========")

    print("\nURL:", result["url"])
    print("Prediction:", result["prediction"])

    print(
        "Phishing probability:",
        result["phishing_probability"], "%"
    )

    print(
        "Risk score:",
        result["risk_score"], "/ 100"
    )

    print("Risk level:", result["risk_level"])

    print("\nRisk indicators:")

    for reason in result["reasons"]:
        print("-", reason)

    print("\nExtracted features:")

    for feature, value in result["features"].items():
        print(f"{feature}: {value}")

    print("\n============================================")
