
import pandas as pd

file_path = "dataset/extracted/PhiUSIIL_Phishing_URL_Dataset.csv"

df = pd.read_csv(file_path)

print("\nDataset loaded successfully!")

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nOriginal label distribution:")
print(df["label"].value_counts().sort_index())

print("\nLabel percentages:")
print(
    df["label"].value_counts(normalize=True).sort_index() * 100
)

print("\nUnique labels:")
print(df["label"].unique())

print("\nDuplicate URLs:")
print(df["URL"].duplicated().sum())
