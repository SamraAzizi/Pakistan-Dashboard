import pandas as pd
import matplotlib.pyplot as plt

# Load the clean data
df = pd.read_csv("data/pakistan_clean.csv")
df['year'] = df['year'].astype(int)
df = df.set_index('year')

# Show basic info
print(df.describe())
print("\nMissing values:\n", df.isna().sum())

# Quick-look plots: one per indicator
fig, axes = plt.subplots(3, 2, figsize=(14, 12))
cols = ['inflation', 'gdp_growth', 'unemployment',
        'education_spend', 'exchange_rate', 'population']

for ax, col in zip(axes.flat, cols):
    df[col].dropna().plot(ax=ax, marker='o')
    ax.set_title(col)
    ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()