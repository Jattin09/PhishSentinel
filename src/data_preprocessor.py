
import pandas as pd


def prepare_dataset(file_path):
    """
    Load, clean and prepare the phishing URL dataset.
    """

    # Load only the columns we need
    df = pd.read_csv(file_path, usecols=["URL", "label"])

    # Remove missing values
    df = df.dropna(subset=["URL", "label"])

    # Remove duplicate URLs
    df = df.drop_duplicates(subset=["URL"])

    # Convert original labels:
    # Original 0 = Phishing
    # Original 1 = Legitimate
    df["label"] = df["label"].map({
        0: 1,
        1: 0
    })

    # Remove any unexpected labels
    df = df.dropna(subset=["label"])

    df["label"] = df["label"].astype(int)

    # Select a balanced, stratified sample
    sample = df.groupby("label", group_keys=False).sample(
        n=10000,
        random_state=42
    )

    return sample.reset_index(drop=True)


if __name__ == "__main__":

    file_path = (
        "dataset/extracted/"
        "PhiUSIIL_Phishing_URL_Dataset.csv"
    )

    data = prepare_dataset(file_path)

    print("\nPrepared dataset:")
    print(data.shape)

    print("\nClass distribution:")
    print(data["label"].value_counts())

    print("\nFirst five records:")
    print(data.head())

print("\nFirst five records:")
print(data.head())

# Save the prepared dataset
output_path = "dataset/processed_urls.csv"

data.to_csv(output_path, index=False)

print(f"\nPrepared dataset saved to: {output_path}")