import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/pakistan_clean.csv")
df['year'] = df['year'].astype(int)
df = df.set_index('year')

# ---------------------------------------------------------------
# INSIGHT 1: Exchange rate devaluation → inflation with a lag
# ---------------------------------------------------------------
print("=" * 60)
print("INSIGHT 1: Devaluation → inflation lag")
print("=" * 60)

df['fx_change'] = df['exchange_rate'].pct_change() * 100

for lag in range(0, 4):
    corr = df['fx_change'].shift(lag).corr(df['inflation'])
    print(f"  Lag {lag} year(s): correlation = {corr:.3f}")

# ---------------------------------------------------------------
# INSIGHT 2: Jobless growth — GDP up, unemployment flat
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("INSIGHT 2: Jobless growth")
print("=" * 60)

df['unemp_change'] = df['unemployment'].diff()
subset = df[['gdp_growth', 'unemp_change']].dropna()
print("Correlation (GDP growth vs change in unemployment):")
print(f"  {subset.corr().iloc[0, 1]:.3f}")
print("\nTop 5 GDP growth years and what unemployment did:")
print(subset.sort_values('gdp_growth', ascending=False).head())

# ---------------------------------------------------------------
# INSIGHT 3: Education spend flat, population growing
# ---------------------------------------------------------------
print("\n" + "=" * 60)
print("INSIGHT 3: Education spend vs population")
print("=" * 60)

print("\nEducation spend (% GDP) — first vs last available:")
print(df['education_spend'].dropna().iloc[[0, -1]])
print("\nPopulation — first vs last:")
print(df['population'].dropna().iloc[[0, -1]])
print("\nPopulation growth rate (% per year, last 10 years):")
print((df['population'].pct_change() * 100).tail(10).round(2))