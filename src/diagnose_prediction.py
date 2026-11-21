
import pandas as pd
from src.feature_extractor import extract_features

url = "https://example.com"

# Extract all nine features
features = extract_features(url)

# Load the updated dataset
df = pd.read_csv("dataset/features.csv")

feature_columns = list(features.keys())

# Find records with exactly matching features
matching_rows = df[
    (df[feature_columns] == pd.Series(features)).all(axis=1)
]

print("\nTest URL:", url)

print("\nExtracted features:")
print(features)

print("\nExact matching records:", len(matching_rows))

if len(matching_rows) > 0:

    print("\nMatching label distribution:")
    print(matching_rows["label"].value_counts())

    print("\nMatching URLs:")

    original_df = pd.read_csv("dataset/processed_urls.csv")

    print(
        original_df.loc[
            matching_rows.index, ["URL", "label"]
        ].to_string(index=False)
    )

else:
    print("\nNo exact matching records found.")
