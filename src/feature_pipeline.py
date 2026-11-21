
import pandas as pd
from src.feature_extractor import extract_features

def generate_feature_dataset(input_path, output_path):
    """
    Extract URL features for every record in the dataset.
    """

    df = pd.read_csv(input_path)

    feature_rows = []

    for url in df["URL"]:
        features = extract_features(url)
        feature_rows.append(features)

    features_df = pd.DataFrame(feature_rows)

    # Preserve the original classification labels
    features_df["label"] = df["label"].values

    features_df.to_csv(output_path, index=False)

    print("Feature generation completed!")
    print("Total records:", len(features_df))
    print("\nGenerated features:")
    print(features_df.head())

    return features_df


if __name__ == "__main__":

    generate_feature_dataset(
        "dataset/processed_urls.csv",
        "dataset/features.csv"
    )
