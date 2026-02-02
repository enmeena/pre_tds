import pandas as pd

# Read files with correct encodings
df1 = pd.read_csv("data1.csv", encoding="cp1252")
df2 = pd.read_csv("data2.csv", encoding="utf-8")
df3 = pd.read_csv("data3.txt", encoding="utf-16", sep="\t")

# Combine all data
df = pd.concat([df1, df2, df3], ignore_index=True)

# Symbols to match
symbols = ["—", "Ÿ", "™"]

# Filter and sum
total_sum = df[df["symbol"].isin(symbols)]["value"].sum()

print(total_sum)