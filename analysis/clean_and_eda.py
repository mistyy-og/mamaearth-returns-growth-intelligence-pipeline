import pandas as pd

print("Python is ready!")
print("Pandas is ready!")

from pathlib import Path
import pandas as pd

downloads = Path.home() / "Downloads"

orders = pd.read_csv(downloads / "orders.csv")
customers = pd.read_csv(downloads / "customers.csv")
products = pd.read_csv(downloads / "products.csv")

print("Orders shape:", orders.shape)
print("Customers shape:", customers.shape)
print("Products shape:", products.shape)

print("\nFirst 5 orders:")
print(orders.head())


print("\n--- ORDERS DATA CHECK ---")

print("\nColumn names:")
print(orders.columns.tolist())

print("\nMissing values:")
print(orders.isnull().sum())

print("\nDuplicate rows:")
print(orders.duplicated().sum())

print("\nFirst 5 rows:")
print(orders.head())


print("\n--- CLEANING ORDERS DATA ---")
orders_clean = orders.copy()


orders_clean["payment_method"] = (
    orders_clean["payment_method"].str.upper().str.strip()
)

# Fill missing discounts with 0
orders_clean["discount_pct"] = orders_clean["discount_pct"].fillna(0)

# Fill missing ratings with the median rating
orders_clean["rating"] = orders_clean["rating"].fillna(
    orders_clean["rating"].median()
)

print("\nMissing values after cleaning:")
print(orders_clean.isnull().sum())

print("\nCleaned orders preview:")
print(orders_clean.head())



print("\n--- DUPLICATE ORDER CHECK ---")

print("Rows before removing duplicates:", len(orders_clean))

# Check duplicate order IDs
print("\nDuplicate order IDs:")
print(orders_clean[
    orders_clean.duplicated(subset=["order_id"], keep=False)
])

# Remove duplicate order IDs, keeping the first occurrence
orders_clean = orders_clean.drop_duplicates(
    subset=["order_id"],
    keep="first"
)

print("\nRows after removing duplicates:", len(orders_clean))
print("Remaining duplicate order IDs:",
      orders_clean["order_id"].duplicated().sum())





print("\n--- MERGING DATASETS ---")

# Connect orders with customer information
orders_customers = orders_clean.merge(
    customers,
    on="customer_id",
    how="left"
)

# Connect the result with product information
full_data = orders_customers.merge(
    products,
    on="product_id",
    how="left"
)

print("\nMerged dataset shape:", full_data.shape)

print("\nMerged column names:")
print(full_data.columns.tolist())

print("\nFirst 5 rows of merged data:")
print(full_data.head())

print("\nMissing values after merging:")
print(full_data.isnull().sum())


print("\n--- REVENUE ANALYSIS ---")

print("Available columns:")
print(full_data.columns.tolist())


full_data["calculated_total"] = (
    full_data["quantity"] * full_data["price"]
)

print("\nTotal calculated revenue:")
print(round(full_data["calculated_total"].sum(), 2))

print("\nRevenue by payment method:")
print(
    full_data.groupby("payment_method")["calculated_total"]
    .sum()
    .round(2)
)




print("\n--- REVENUE ANALYSIS ---")

full_data["calculated_total"] = (
    full_data["quantity"] * full_data["price"]
)

print("\nTotal calculated revenue:")
print(round(full_data["calculated_total"].sum(), 2))

print("\nRevenue by payment method:")
print(
    full_data.groupby("payment_method")["calculated_total"]
    .sum()
    .round(2)
)


print("\n--- REVENUE WITH DISCOUNTS ---")

full_data["discounted_total"] = (
    full_data["quantity"]
    * full_data["price"]
    * (1 - full_data["discount_pct"] / 100)
)

print(
    "Revenue before discounts:",
    round(full_data["calculated_total"].sum(), 2)
)

print(
    "Revenue after discounts:",
    round(full_data["discounted_total"].sum(), 2)

)




print("\n--- RECONCILED REVENUE CHECK ---")


full_data["discounted_total"] = (
    full_data["quantity"]
    * full_data["price"]
    * (1 - full_data["discount_pct"] / 100)
)

print(
    "Revenue after deduplication:",
    round(full_data["discounted_total"].sum(), 2)
)

print("Number of rows in merged dataset:", len(full_data))




print("\n--- FINAL DEDUPLICATION CHECK ---")

print("Rows before deduplication:", len(full_data))

duplicate_ids = ["O0176", "O0177", "O0178", "O0179", "O0180"]

full_data_clean = full_data[
    ~full_data["order_id"].isin(duplicate_ids)
].copy()

print("Rows after deduplication:", len(full_data_clean))

print(
    "Revenue after deduplication:",
    round(full_data_clean["discounted_total"].sum(), 2)
)




print("\n--- QUANTITY OUTLIER ANALYSIS ---")

Q1 = full_data_clean["quantity"].quantile(0.25)
Q3 = full_data_clean["quantity"].quantile(0.75)

IQR = Q3 - Q1

lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

print("Q1:", Q1)
print("Q3:", Q3)
print("IQR:", IQR)
print("Lower bound:", lower_bound)
print("Upper bound:", upper_bound)

outliers = full_data_clean[
    (full_data_clean["quantity"] < lower_bound)
    | (full_data_clean["quantity"] > upper_bound)
]

print("\nQuantity outliers:")
print(outliers[["order_id", "quantity"]])
print("Number of outlier rows:", len(outliers))



print("\n--- RETURN ANALYSIS ---")

print("Available columns:")
print(full_data_clean.columns.tolist())

print("\nReturn counts by payment method:")

print(
    full_data_clean.groupby("payment_method")["returned"]
    .value_counts()
)

print("\nReturn rate by payment method (%):")

return_rates = (
    full_data_clean.groupby("payment_method")["returned"]
    .mean()
    .mul(100)
    .round(2)
)

print(return_rates)





print("\n--- COD RETURNS BY CITY TIER ---")

cod_data = full_data_clean[
    full_data_clean["payment_method"] == "COD"
]

cod_tier_analysis = (
    cod_data.groupby("city_tier")["returned"]
    .agg(["count", "sum", "mean"])
)

cod_tier_analysis["return_rate_pct"] = (
    cod_tier_analysis["mean"] * 100
).round(2)

print(cod_tier_analysis)






print("\n--- CORRELATION ANALYSIS ---")

numeric_columns = [
    "quantity",
    "discount_pct",
    "rating",
    "returned",
    "price"
]

correlation_matrix = full_data_clean[numeric_columns].corr()

print(correlation_matrix.round(3))

print("\nDiscount vs returned correlation:")
print(
    round(
        correlation_matrix.loc["discount_pct", "returned"],
        3
    )
)



print("\n--- SAVING CLEANED DATA ---")

from pathlib import Path

output_path = Path.home() / "Downloads" / "cleaned_orders_analysis.csv"

full_data_clean.to_csv(output_path, index=False)

print("Cleaned dataset saved to:")
print(output_path)
print("Final rows:", len(full_data_clean))




import json
from pathlib import Path

# Export findings to the narrator folder in Documents
narrator_folder = Path.home() / "Documents" / "narrator"
narrator_folder.mkdir(parents=True, exist_ok=True)

findings = {
    "cleaned_total_revenue_inr": 97358.30,
    "raw_total_revenue_inr": 99860.20,
    "duplicate_reconciliation_delta_inr": 2501.90,
    "return_rate_by_payment": {
        "COD": 44.4,
        "CARD": 14.7,
        "UPI": 18.9
    },
    "highest_risk_segment": {
        "payment_method": "COD",
        "city_tier": 2,
        "return_rate_pct": 54.5
    },
    "true_peak_month": {
        "month": "2026-03",
        "revenue_inr": 20318.90
    },
    "outlier_inflated_month": {
        "month": "2026-01",
        "apparent_revenue_inr": 29582.10,
        "corrected_revenue_inr": 11637.10
    }
}

findings_path = narrator_folder / "findings.json"

with findings_path.open("w", encoding="utf-8") as file:
    json.dump(findings, file, indent=4)

print("Findings exported to:", findings_path)





# ==========================================
# PART 3: EXPORT FINDINGS FOR THE NARRATOR
# ==========================================

import json
from pathlib import Path
import pandas as pd

# Use the DataFrames created in Part 2.
raw_data = full_data.copy()
clean_data = full_data_clean.copy()

# Ensure dates are in the correct format.
raw_data["order_date"] = pd.to_datetime(raw_data["order_date"])
clean_data["order_date"] = pd.to_datetime(clean_data["order_date"])

# Convert the returned column to numeric 0/1 values.
def make_return_flag(series):
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(0).astype(int)

    return (
        series.astype(str).str.strip().str.lower()
        .map({
            "true": 1, "false": 0,
            "yes": 1, "no": 0,
            "1": 1, "0": 0,
            "returned": 1, "not returned": 0
        })
    )

clean_data["return_flag"] = make_return_flag(clean_data["returned"])

if clean_data["return_flag"].isna().any():
    raise ValueError(
        "Some return values could not be interpreted. "
        "Check the returned column before exporting."
    )

# Revenue reconciliation.
raw_revenue = round(float(raw_data["discounted_total"].sum()), 2)
clean_revenue = round(float(clean_data["discounted_total"].sum()), 2)
reconciliation_delta = round(raw_revenue - clean_revenue, 2)

# Return rate by payment method.
payment_rates = (
    clean_data.groupby("payment_method")["return_flag"]
    .mean().mul(100).round(1)
)

# Highest-risk payment method and city tier.
segment_rates = (
    clean_data.groupby(["payment_method", "city_tier"])["return_flag"]
    .agg(["mean", "count"])
    .reset_index()
)
segment_rates["return_rate_pct"] = (
    segment_rates["mean"] * 100
).round(1)

highest_risk = segment_rates.sort_values(
    ["return_rate_pct", "count"],
    ascending=[False, False]
).iloc[0]

# Identify quantity outliers using the IQR rule.
q1 = clean_data["quantity"].quantile(0.25)
q3 = clean_data["quantity"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outlier_mask = (
    (clean_data["quantity"] < lower_bound)
    | (clean_data["quantity"] > upper_bound)
)

outlier_ids = clean_data.loc[outlier_mask, "order_id"].unique()

# Compare monthly revenue before and after excluding quantity outliers.
clean_data["month"] = clean_data["order_date"].dt.strftime("%Y-%m")

corrected_data = clean_data.loc[~outlier_mask].copy()
corrected_data["month"] = corrected_data["order_date"].dt.strftime("%Y-%m")

apparent_monthly = clean_data.groupby("month")["discounted_total"].sum()
corrected_monthly = corrected_data.groupby("month")["discounted_total"].sum()

monthly_comparison = pd.DataFrame({
    "apparent_revenue": apparent_monthly,
    "corrected_revenue": corrected_monthly
}).fillna(0)

monthly_comparison["difference"] = (
    monthly_comparison["apparent_revenue"]
    - monthly_comparison["corrected_revenue"]
)

# Month with the highest corrected revenue.
true_peak_month = corrected_monthly.idxmax()

# Month whose revenue was most affected by quantity outliers.
outlier_month = monthly_comparison["difference"].idxmax()

findings = {
    "cleaned_total_revenue_inr": round(
        float(clean_revenue), 2
    ),
    "raw_total_revenue_inr": round(
        float(raw_revenue), 2
    ),
    "duplicate_reconciliation_delta_inr": round(
        float(reconciliation_delta), 2
    ),
    "return_rate_by_payment": {
        method: round(float(payment_rates[method]), 1)
        for method in ["COD", "CARD", "UPI"]
    },
    "highest_risk_segment": {
        "payment_method": str(highest_risk["payment_method"]),
        "city_tier": int(highest_risk["city_tier"]),
        "return_rate_pct": float(highest_risk["return_rate_pct"])
    },
    "true_peak_month": {
        "month": str(true_peak_month),
        "revenue_inr": round(
            float(corrected_monthly[true_peak_month]), 2
        )
    },
    "outlier_inflated_month": {
        "month": str(outlier_month),
        "apparent_revenue_inr": round(
            float(monthly_comparison.loc[outlier_month, "apparent_revenue"]), 2
        ),
        "corrected_revenue_inr": round(
            float(monthly_comparison.loc[outlier_month, "corrected_revenue"]), 2
        )
    }
}

# Save findings.json in Documents/narrator.
narrator_folder = Path.home() / "OneDrive" / "Desktop" / "data" / "narrator"
narrator_folder.mkdir(parents=True, exist_ok=True)

findings_path = narrator_folder / "findings.json"

with findings_path.open("w", encoding="utf-8") as file:
    json.dump(findings, file, indent=4)

print("\n--- PART 3 FINDINGS EXPORTED ---")
print("File:", findings_path)
print(json.dumps(findings, indent=4))
print("Quantity outlier order IDs:", list(outlier_ids))






