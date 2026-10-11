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

if date_col is None:
    raise ValueError("Could not find date column. Check your raw data.")

df = df.rename(columns={date_col: 'year'})

# 4. Convert year to integer
df['year'] = pd.to_numeric(df['year'], errors='coerce').astype('Int64')

# 5. Drop any rows where year is NaN
df = df.dropna(subset=['year'])

# 6. Sort by year
df = df.sort_values('year').reset_index(drop=True)

# 7. Check missing values
print("\nMissing values per column:")
print(df.isna().sum())

# 8. For missing values, we'll keep them for now
# (We'll decide on imputation strategy after EDA)

# 9. Save the cleaned data
df.to_csv("data/pakistan_clean.csv", index=False)

print("\nCleaned shape:", df.shape)
print("Cleaned columns:", df.columns.tolist())
print("\nFirst 5 rows of cleaned data:")
print(df.head())