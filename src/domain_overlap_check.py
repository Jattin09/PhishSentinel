
import pandas as pd
from urllib.parse import urlsplit


# Load prepared URLs
df = pd.read_csv("dataset/processed_urls.csv")


def get_hostname(url):
    if "://" not in url:
        url = "https://" + url

    return urlsplit(url).hostname


# Extract hostnames
df["hostname"] = df["URL"].apply(get_hostname)

# Randomly split records using the same seed
train = df.sample(frac=0.8, random_state=42)
test = df.drop(train.index)

# Compare unique hostnames
train_domains = set(train["hostname"])
test_domains = set(test["hostname"])

overlap = train_domains.intersection(test_domains)

print("\nTraining records:", len(train))
print("Testing records:", len(test))

print("\nUnique training domains:", len(train_domains))
print("Unique testing domains:", len(test_domains))

print("\nDomains appearing in both sets:", len(overlap))

if len(test_domains) > 0:
    percentage = len(overlap) / len(test_domains) * 100
    print("Test domain overlap:", round(percentage, 2), "%")

print("\nSample overlapping domains:")

for domain in sorted(overlap)[:20]:
    print(domain)