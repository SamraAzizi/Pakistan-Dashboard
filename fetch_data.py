import wbdata
import pandas as pandas
from datetime import datetime

# defining what we want
indicators = {
    "FP.CPI.TOTL.ZG": "inflation",
    "NY.GDP.MKTP.KD.ZG": "gdp_growth",
    "SL.UEM.TOTL.ZS": "unemployment",
    "SE.XPD.TOTL.GD.ZS": "education_spend",
    "PA.NUS.FCRF": "exchange_rate",
    "SP.POP.TOTL": "population"

}

# defining where and when we want

country = "PAK"  # Pakistan ISO3 code
start_year = 1990
end_year = 2023

# fetch into a dataframe

print("fetching data from world bank api,")
df = wbdata.get_dataframe(
    indicators, 
    country=country,
    date=(str(start_year), str(end_year))
)

# inspect what we want
print("\nShape:", df.shape)
print("\nColumns:", df.columns.tolist())
print("\nFirst 5 rows:")
print(df.head())
print("\nLast 5 rows:")
print(df.tail())
print("\nMissing values per column:")
print(df.isna().sum())

# 5. Save raw data
df.to_csv("data/pakistan_raw.csv")
print("\nSaved to data/pakistan_raw.csv")