
import pandas as pd

# STEP 1: LOAD DATASET
print("\n========== STEP 1: LOAD DATASET ==========")

df = pd.read_excel("Online Retail.xlsx")

print("Original dataset shape:", df.shape)
print(df.head())


# STEP 2: EXPLORE DATASET
print("\n========== STEP 2: DATASET INFORMATION ==========")

print("\nColumn names:")
print(df.columns)

print("\nData types:")
print(df.dtypes)

print("\nDataset information:")
df.info()


# STEP 3: CHECK MISSING VALUES
print("\n========== STEP 3: MISSING VALUES ==========")

print(df.isnull().sum())

print("\nMissing value percentages:")
print((df.isnull().sum() / len(df) * 100).round(2))


# STEP 4: CHECK DUPLICATES
print("\n========== STEP 4: DUPLICATE RECORDS ==========")

print("Duplicate rows before cleaning:", df.duplicated().sum())

df = df.drop_duplicates()

print("Rows after removing duplicates:", len(df))
print("Duplicate rows remaining:", df.duplicated().sum())


# STEP 5: FIX MISSING DESCRIPTIONS
print("\n========== STEP 5: MISSING DESCRIPTIONS ==========")

before = df["Description"].isnull().sum()

description_map = (
    df.dropna(subset=["Description"])
      .groupby("StockCode")["Description"]
      .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else None)
)

missing = df["Description"].isnull()

df.loc[missing, "Description"] = (
    df.loc[missing, "StockCode"].map(description_map)
)

after = df["Description"].isnull().sum()

print("Missing descriptions before:", before)
print("Missing descriptions after:", after)
print("Descriptions filled:", before - after)


# STEP 6: HANDLE MISSING CUSTOMER IDs
print("\n========== STEP 6: CUSTOMER IDs ==========")

print("Missing CustomerID values:", df["CustomerID"].isnull().sum())

# Keep missing CustomerID values.
# Do not invent customer IDs or delete these rows.


# STEP 7: CHECK INVALID QUANTITIES AND PRICES
print("\n========== STEP 7: INVALID VALUES ==========")

print("Zero or negative quantities:",
      (df["Quantity"] <= 0).sum())

print("Zero or negative unit prices:",
      (df["UnitPrice"] <= 0).sum())


# STEP 8: REMOVE INVALID PRICES AND ZERO QUANTITIES
print("\n========== STEP 8: DATA FILTERING ==========")

before_filtering = len(df)

# Remove zero or negative prices.
# Remove zero quantities.
# Keep negative quantities because they can represent product returns.

df = df[
    (df["UnitPrice"] > 0) &
    (df["Quantity"] != 0)
].copy()

print("Rows before filtering:", before_filtering)
print("Rows after filtering:", len(df))
print("Rows removed:", before_filtering - len(df))


# STEP 9: CONVERT CUSTOMER ID DATA TYPE
print("\n========== STEP 9: DATA TYPE CONVERSION ==========")

df["CustomerID"] = df["CustomerID"].astype("Int64")

print(df.dtypes)


# STEP 10: CREATE TOTAL SALES COLUMN
print("\n========== STEP 10: FEATURE CREATION ==========")

df["TotalSales"] = (df["Quantity"] * df["UnitPrice"]).round(2)

print(df[["Quantity", "UnitPrice", "TotalSales"]].head())


# STEP 11: CHECK FINAL MISSING VALUES
print("\n========== STEP 11: FINAL MISSING VALUES ==========")

print(df.isnull().sum())


# STEP 12: FINAL DATASET SUMMARY
print("\n========== STEP 12: FINAL DATASET ==========")

print("Final dataset shape:", df.shape)

print("\nFinal dataset information:")
df.info()

print("\nFinal dataset preview:")
print(df.head())


# STEP 13: EXPORT CLEANED DATASET
print("\n========== STEP 13: EXPORT CSV ==========")

df.to_csv("cleaned_online_retail.csv", index=False)

print("Cleaned dataset saved successfully!")
print("File name: cleaned_online_retail.csv")


# FINAL SUMMARY
print("\n========== CLEANING SUMMARY ==========")

print("Original rows: 541909")
print("Final rows:", len(df))
print("Remaining duplicates:", df.duplicated().sum())
print("Remaining missing descriptions:",
      df["Description"].isnull().sum())
print("Remaining missing CustomerIDs:",
      df["CustomerID"].isnull().sum())

print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")
print("\n========== FINAL VERIFICATION ==========")

print("Final number of rows:", len(df))
print("Final number of columns:", len(df.columns))

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nTotal sales:")
print(round(df["TotalSales"].sum(), 2))

print("\nDate range:")
print(df["InvoiceDate"].min())
print(df["InvoiceDate"].max())

print("\nCountry count:", df["Country"].nunique())

print("\nCSV exported successfully!")