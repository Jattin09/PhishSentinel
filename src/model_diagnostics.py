
import joblib
import pandas as pd

from src.feature_extractor import extract_features


# Load the saved Random Forest model
model = joblib.load("models/phishing_model.pkl")

# Analyse the example URL
url = "https://example.com"

# Extract features
features = extract_features(url)

# Prepare model input
input_data = pd.DataFrame([features])

# Get prediction
prediction = model.predict(input_data)[0]

# Get probabilities
probabilities = model.predict_proba(input_data)[0]

print("\n========== MODEL DIAGNOSTICS ==========")

print("\nURL:", url)

print("\nExtracted features:")
for feature, value in features.items():
    print(f"{feature}: {value}")

print("\nModel prediction:", prediction)

print("\nModel classes:", model.classes_)

print("\nPrediction probabilities:")

for class_label, probability in zip(
    model.classes_, probabilities
):
    name = "Phishing" if class_label == 1 else "Legitimate"
    print(f"{name}: {probability * 100:.2f}%")

# Examine individual decision-tree votes
tree_predictions = [
    tree.predict(input_data)[0]
    for tree in model.estimators_
]

phishing_votes = tree_predictions.count(1)
legitimate_votes = tree_predictions.count(0)

print("\nIndividual tree votes:")
print("Phishing votes:", phishing_votes)
print("Legitimate votes:", legitimate_votes)
print("Total trees:", len(model.estimators_))

print("\n=======================================")
