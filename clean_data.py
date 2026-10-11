import pandas as pd

# 1. Load the raw data
df = pd.read_csv("data/pakistan_raw.csv")

print("Original shape:", df.shape)
print("Original columns:", df.columns.tolist())
print("\nFirst 3 rows:")
print(df.head(3))

# 2. Flatten the index if it's a MultiIndex
if isinstance(df.index, pd.MultiIndex):
    df = df.reset_index()

# 3. Identify and rename the date column
# The date column might be named 'date' or something similar
date_col = None
for col in df.columns:
    if 'date' in col.lower() or 'year' in col.lower():
        date_col = col
        break