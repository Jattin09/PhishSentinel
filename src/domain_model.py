
import pandas as pd
from urllib.parse import urlsplit

from sklearn.model_selection import GroupShuffleSplit
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)


def get_hostname(url):
    """Extract hostname from URL."""

    if "://" not in url:
        url = "https://" + url

    return urlsplit(url).hostname


def prepare_domain_split():

    urls_df = pd.read_csv("dataset/processed_urls.csv")
    features_df = pd.read_csv("dataset/features.csv")

    groups = urls_df["URL"].apply(get_hostname)

    X = features_df.drop("label", axis=1)
    y = features_df["label"]

    splitter = GroupShuffleSplit(
        n_splits=1,
        test_size=0.20,
        random_state=42
    )

    train_indices, test_indices = next(
        splitter.split(X, y, groups=groups)
    )

    X_train = X.iloc[train_indices]
    X_test = X.iloc[test_indices]

    y_train = y.iloc[train_indices]
    y_test = y.iloc[test_indices]

    train_domains = set(groups.iloc[train_indices])
    test_domains = set(groups.iloc[test_indices])

    overlap = train_domains.intersection(test_domains)

    print("Training records:", len(X_train))
    print("Testing records:", len(X_test))
    print("Overlapping domains:", len(overlap))

    print("\nTraining label distribution:")
    print(y_train.value_counts())

    print("\nTesting label distribution:")
    print(y_test.value_counts())

    return X_train, X_test, y_train, y_test


def train_and_evaluate():

    X_train, X_test, y_train, y_test = prepare_domain_split()

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced"
    )

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print("\nDomain-based model accuracy:")
    print(accuracy_score(y_test, predictions) * 100, "%")

    print("\nClassification Report:")

    print(classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Legitimate", "Phishing"],
        zero_division=0
    ))

    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, predictions))


if __name__ == "__main__":
    train_and_evaluate()
