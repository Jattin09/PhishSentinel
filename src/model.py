import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)
import pandas as pd


def prepare_training_data(file_path):
    """Load features and split into training and testing data."""

    df = pd.read_csv(file_path)

    X = df.drop("label", axis=1)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("Training records:", len(X_train))
    print("Testing records:", len(X_test))

    return X_train, X_test, y_train, y_test


def train_model(X_train, y_train):
    """Train the Random Forest classifier."""

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    print("\nModel training completed!")

    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model performance."""

    predictions = model.predict(X_test)

    accuracy = accuracy_score(y_test, predictions)

    print("\nModel Accuracy:", accuracy * 100, "%")

    print("\nClassification Report:")

    print(classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Legitimate", "Phishing"]
    ))

    print("\nConfusion Matrix:")

    print(confusion_matrix(y_test, predictions, labels=[0, 1]))


if __name__ == "__main__":

    X_train, X_test, y_train, y_test = prepare_training_data(
        "dataset/features.csv"
    )

    model = train_model(X_train, y_train)
    joblib.dump(model, "models/phishing_model.pkl")

print("\nModel saved successfully!")

evaluate_model(model, X_test, y_test)
