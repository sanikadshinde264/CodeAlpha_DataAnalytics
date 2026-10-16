"""
CodeAlpha_ECommerce_EDA
E-Commerce Sales & Customer Insights - Exploratory Data Analysis
Dataset: ecommerce_customer_data_custom_ratios.csv (Kaggle)
Libraries: Pandas, NumPy, Matplotlib, Seaborn, SciPy
"""

import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")          # saves charts to files (no pop-up windows)
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------------------------------------------------
# STEP 0: SETTINGS
# ----------------------------------------------------------------------
DATA_FILES = [
    "data/ecommerce_customer_data_custom_ratios.csv",
    "data/ecommerce_data.csv",
]
FIG_DIR = "figures"
os.makedirs(FIG_DIR, exist_ok=True)

sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams["figure.figsize"] = (10, 5)


def header(text):
    print("\n" + "=" * 70)
    print(text)
    print("=" * 70)


def save_fig(name):
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, name), dpi=150)
    plt.close()


# ----------------------------------------------------------------------
# STEP 1: LOAD DATA
# ----------------------------------------------------------------------
header("STEP 1: LOADING DATA")
path = next((p for p in DATA_FILES if os.path.exists(p)), None)
if path is None:
    raise FileNotFoundError(
        "Dataset not found. Put the CSV inside the 'data' folder as "
        "'ecommerce_customer_data_custom_ratios.csv'."
    )
raw = pd.read_csv(path)
print("Loaded:", path)

df = raw.rename(columns={
    "Customer ID": "customer_id",
    "Purchase Date": "purchase_date",
    "Product Category": "category",
    "Product Price": "unit_price",
    "Quantity": "quantity",
    "Total Purchase Amount": "revenue",
    "Payment Method": "payment_method",
    "Customer Age": "customer_age",
    "Returns": "returns",
    "Customer Name": "customer_name",
    "Age": "age_dup",
    "Gender": "gender",
    "Churn": "churn",
}).copy()

# ----------------------------------------------------------------------
# STEP 2: UNDERSTAND THE DATA STRUCTURE
# ----------------------------------------------------------------------
header("STEP 2: DATA STRUCTURE")
print("Shape (rows, columns):", df.shape)
print("\nFirst 5 rows:\n", df.head().to_string())
print("\nData types / non-null counts:")
df.info()
print("\nNumeric summary:\n", df.describe().T.round(2).to_string())
print("\nCategorical columns:")
for col in ["category", "payment_method", "gender"]:
    print(f"  {col}: {df[col].nunique()} values -> {sorted(df[col].unique())}")

# ----------------------------------------------------------------------
# STEP 3: DATA QUALITY CHECK
# ----------------------------------------------------------------------
header("STEP 3: DATA QUALITY CHECK")
missing = df.isnull().sum()
missing_tbl = pd.DataFrame({"missing": missing, "percent": (missing / len(df) * 100).round(2)})
print("Missing values:\n", missing_tbl[missing > 0].to_string())
print("\nDuplicate rows:", df.duplicated().sum())
print("Are 'customer_age' and 'Age' identical?", bool((df["customer_age"] == df["age_dup"]).all()))

df["purchase_date"] = pd.to_datetime(df["purchase_date"], errors="coerce")
print("Unparseable dates:", df["purchase_date"].isnull().sum())
print("Date range:", df["purchase_date"].min().date(), "to", df["purchase_date"].max().date())

calc_amount = df["unit_price"] * df["quantity"]
mismatch = (calc_amount != df["revenue"]).mean() * 100
print(f"\nRows where Total Purchase Amount != Price x Quantity: {mismatch:.1f}%")
print("-> The recorded total includes other factors (or the data is synthetic), so we use")
print("   'Total Purchase Amount' as revenue, as it is the amount recorded for each purchase.")

plt.figure(figsize=(8, 4))
sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap="viridis")
plt.title("Missing Values Map (yellow = missing)")
save_fig("01_missing_values.png")

# ----------------------------------------------------------------------
# STEP 4: DATA CLEANING
# ----------------------------------------------------------------------
header("STEP 4: CLEANING")
before = len(df)
df = df.drop_duplicates()
print(f"Removed {before - len(df)} duplicate rows")

df = df.drop(columns=["age_dup"])            # identical copy of customer_age
df = df.dropna(subset=["purchase_date"])
df = df[(df["quantity"] > 0) & (df["unit_price"] > 0) & (df["revenue"] > 0)]

# 'returns' is missing for ~19% of rows: we do NOT guess. We keep a flag and
# calculate return rates only on rows where the value is known.
df["returns_known"] = df["returns"].notna()
print(f"'returns' missing for {(~df['returns_known']).mean()*100:.1f}% of rows -> kept as unknown")

# The data has no order ID: each row is one purchase (transaction)
df = df.reset_index(drop=True)
df["order_id"] = df.index + 1
print("Rows after cleaning:", len(df))

# ----------------------------------------------------------------------
# STEP 5: FEATURE ENGINEERING
# ----------------------------------------------------------------------
df["year"] = df["purchase_date"].dt.year
df["month"] = df["purchase_date"].dt.month
df["quarter"] = df["purchase_date"].dt.quarter
df["weekday"] = df["purchase_date"].dt.day_name()
df["hour"] = df["purchase_date"].dt.hour
df["year_month"] = df["purchase_date"].dt.to_period("M").astype(str)
df["year_quarter"] = df["purchase_date"].dt.to_period("Q").astype(str)
df["age_group"] = pd.cut(
    df["customer_age"], bins=[17, 24, 34, 44, 54, 64, 70],
    labels=["18-24", "25-34", "35-44", "45-54", "55-64", "65-70"],
)
df["price_band"] = pd.cut(
    df["unit_price"], bins=[0, 100, 200, 300, 400, 500],
    labels=["10-100", "101-200", "201-300", "301-400", "401-500"],
)

# ----------------------------------------------------------------------
# STEP 6: OUTLIER DETECTION (IQR method)
# ----------------------------------------------------------------------
header("STEP 6: OUTLIERS (IQR method)")
for col in ["unit_price", "quantity", "revenue", "customer_age"]:
    q1, q3 = df[col].quantile([0.25, 0.75])
    iqr = q3 - q1
    low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    n_out = int(((df[col] < low) | (df[col] > high)).sum())
    print(f"{col:<13} bounds=({low:.1f}, {high:.1f})  outliers={n_out} ({n_out/len(df)*100:.2f}%)")

fig, axes = plt.subplots(1, 4, figsize=(16, 4))
for ax, col in zip(axes, ["unit_price", "quantity", "revenue", "customer_age"]):
    sns.boxplot(y=df[col], ax=ax, color="#5ec962")
    ax.set_title(col)
plt.suptitle("Outlier Check (boxplots)")
save_fig("02_outliers_boxplots.png")

# ----------------------------------------------------------------------
# STEP 7: SALES TRENDS - MONTHLY, QUARTERLY, YEARLY
# ----------------------------------------------------------------------
header("STEP 7: SALES TRENDS")
monthly = df.groupby("year_month")["revenue"].sum()
quarterly = df.groupby("year_quarter")["revenue"].sum()
yearly = df.groupby("year")["revenue"].agg(["sum", "count"])
print("Yearly revenue and orders:\n", yearly.round(0).to_string())
print("\nTop 5 months by revenue:\n", monthly.sort_values(ascending=False).head(5).round(0).to_string())
print("\nQuarterly revenue:\n", quarterly.round(0).to_string())

plt.figure(figsize=(14, 5))
monthly.plot(marker="o", markersize=3, color="#31688e")
plt.title("Monthly Revenue Trend"); plt.xlabel("Month"); plt.ylabel("Revenue")
plt.xticks(rotation=60)
save_fig("03_monthly_sales_trend.png")

plt.figure(figsize=(12, 5))
quarterly.plot(kind="bar", color="#35b779")
plt.title("Quarterly Revenue"); plt.xlabel("Quarter"); plt.ylabel("Revenue")
plt.xticks(rotation=60)
save_fig("04_quarterly_sales.png")

season = df.groupby(["year", "month"])["revenue"].sum().groupby("month").mean()
plt.figure(figsize=(10, 5))
sns.barplot(x=season.index, y=season.values, color="#440154")
plt.title("Seasonality: Average Monthly Revenue by Calendar Month")
plt.xlabel("Month (1 = Jan)"); plt.ylabel("Average revenue")
save_fig("05_seasonality.png")

# ----------------------------------------------------------------------
# STEP 8: TOP-SELLING CATEGORIES & PRICE BANDS
# (this dataset has no product names, so we use category and price band)
# ----------------------------------------------------------------------
header("STEP 8: TOP-SELLING CATEGORIES / PRICE BANDS")
cat_units = df.groupby("category")["quantity"].sum().sort_values(ascending=False)
cat_rev = df.groupby("category")["revenue"].sum().sort_values(ascending=False)
band = df.groupby("price_band", observed=True).agg(units=("quantity", "sum"), revenue=("revenue", "sum"))
print("Units sold by category:\n", cat_units.to_string())
print("\nRevenue by price band:\n", band.round(0).to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(x=cat_units.values, y=cat_units.index, ax=axes[0], color="#21918c")
axes[0].set_title("Units Sold by Category")
sns.barplot(x=band.index.astype(str), y=band["revenue"], ax=axes[1], color="#fde725")
axes[1].set_title("Revenue by Unit-Price Band"); axes[1].set_xlabel("Unit price band")
save_fig("06_top_categories_and_price_bands.png")

# ----------------------------------------------------------------------
# STEP 9: REVENUE & "PROFITABILITY" BY CATEGORY
# No cost column exists, so true profit cannot be computed. We compare
# categories using revenue, average order value and return rate instead.
# ----------------------------------------------------------------------
header("STEP 9: CATEGORY ANALYSIS")
cat = df.groupby("category").agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    avg_order_value=("revenue", "mean"),
    units=("quantity", "sum"),
)
cat["share_of_revenue_%"] = cat["revenue"] / cat["revenue"].sum() * 100
cat["return_rate_%"] = df[df["returns_known"]].groupby("category")["returns"].mean() * 100
cat["revenue_after_returns"] = df.assign(
    kept=np.where(df["returns"] == 1, 0, df["revenue"])
).groupby("category")["kept"].sum()
cat = cat.sort_values("revenue", ascending=False)
print(cat.round(2).to_string())
print("\nNote: no cost data -> 'most profitable' is approximated by revenue kept after returns.")

fig, axes = plt.subplots(1, 3, figsize=(17, 5))
sns.barplot(x=cat.index, y=cat["revenue"], ax=axes[0], color="#3b528b")
axes[0].set_title("Total Revenue by Category")
sns.barplot(x=cat.index, y=cat["avg_order_value"], ax=axes[1], color="#21918c")
axes[1].set_title("Average Order Value by Category")
sns.barplot(x=cat.index, y=cat["return_rate_%"], ax=axes[2], color="#fde725")
axes[2].set_title("Return Rate (%) by Category")
save_fig("07_category_analysis.png")

# ----------------------------------------------------------------------
# STEP 10: CUSTOMER AGE / GENDER PATTERNS
# ----------------------------------------------------------------------
header("STEP 10: CUSTOMER AGE / GENDER PATTERNS")
cust = df.groupby("customer_id").agg(
    age=("customer_age", "first"),
    gender=("gender", "first"),
    churn=("churn", "max"),
    total_spent=("revenue", "sum"),
    orders=("order_id", "count"),
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.histplot(cust["age"], bins=26, kde=True, ax=axes[0], color="#440154")
axes[0].set_title("Customer Age Distribution")
gc = cust["gender"].value_counts()
axes[1].pie(gc, labels=gc.index, autopct="%1.1f%%", startangle=90,
            colors=sns.color_palette("viridis", len(gc)))
axes[1].set_title("Customer Gender Split")
save_fig("08_customer_demographics.png")

age_tbl = df.groupby("age_group", observed=True)["revenue"].agg(["sum", "mean", "count"]).round(2)
gender_tbl = df.groupby("gender")["revenue"].agg(["sum", "mean", "count"]).round(2)
print("Revenue by age group:\n", age_tbl.to_string())
print("\nRevenue by gender:\n", gender_tbl.to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(x=age_tbl.index.astype(str), y=age_tbl["sum"], ax=axes[0], color="#31688e")
axes[0].set_title("Total Revenue by Age Group"); axes[0].set_xlabel("Age group")
sns.barplot(data=df, x="category", y="revenue", hue="gender", estimator="sum",
            errorbar=None, ax=axes[1])
axes[1].set_title("Category Revenue by Gender")
save_fig("09_age_gender_spending.png")

pref = df.pivot_table(index="age_group", columns="category", values="revenue",
                      aggfunc="sum", observed=True)
pref_pct = pref.div(pref.sum(axis=1), axis=0) * 100
plt.figure(figsize=(9, 5))
sns.heatmap(pref_pct, annot=True, fmt=".1f", cmap="viridis")
plt.title("Category Preference by Age Group (% of the group's revenue)")
save_fig("10_age_category_heatmap.png")

# ----------------------------------------------------------------------
# STEP 11: AVERAGE ORDER VALUE (AOV) + HYPOTHESIS TESTS
# ----------------------------------------------------------------------
header("STEP 11: AVERAGE ORDER VALUE")
aov = df["revenue"].mean()
print(f"Overall Average Order Value: {aov:,.2f}")
print(f"Median Order Value:          {df['revenue'].median():,.2f}")
print("\nAOV by payment method:\n", df.groupby("payment_method")["revenue"].mean().round(2).to_string())
print("\nAOV by gender:\n", df.groupby("gender")["revenue"].mean().round(2).to_string())

aov_month = df.groupby("year_month")["revenue"].mean()
plt.figure(figsize=(14, 5))
aov_month.plot(marker="o", markersize=3, color="#35b779")
plt.axhline(aov, color="red", linestyle="--", label=f"Overall AOV = {aov:,.0f}")
plt.title("Average Order Value Over Time"); plt.xticks(rotation=60); plt.legend()
save_fig("11_aov_over_time.png")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
sns.barplot(data=df, x="payment_method", y="revenue", errorbar=None, ax=axes[0], color="#3b528b")
axes[0].set_title("AOV by Payment Method")
sns.histplot(df["revenue"], bins=40, kde=True, ax=axes[1], color="#440154")
axes[1].set_title("Distribution of Order Value")
save_fig("12_aov_payment_distribution.png")

try:
    from scipy import stats
    male = df.loc[df["gender"] == "Male", "revenue"]
    female = df.loc[df["gender"] == "Female", "revenue"]
    _, p_g = stats.mannwhitneyu(male, female, alternative="two-sided")
    print(f"\nHypothesis test 1 (Mann-Whitney U): order value Male vs Female, p = {p_g:.4f}")
    print("  ->", "Significant difference" if p_g < 0.05 else "No significant difference at 5% level")
    groups = [g["revenue"].values for _, g in df.groupby("category")]
    _, p_c = stats.kruskal(*groups)
    print(f"Hypothesis test 2 (Kruskal-Wallis): order value differs across categories, p = {p_c:.4f}")
    print("  ->", "Significant difference" if p_c < 0.05 else "No significant difference at 5% level")
except ImportError:
    print("\n(scipy not installed - skipping hypothesis tests: pip install scipy)")

# ----------------------------------------------------------------------
# STEP 12: CORRELATION BETWEEN NUMERICAL VARIABLES
# ----------------------------------------------------------------------
header("STEP 12: CORRELATION")
num_cols = ["unit_price", "quantity", "revenue", "customer_age", "returns", "churn"]
corr = df[num_cols].corr()
print(corr.round(3).to_string())

plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, square=True)
plt.title("Correlation Matrix")
save_fig("13_correlation_heatmap.png")

plt.figure(figsize=(8, 5))
sample = df.sample(5000, random_state=1)
sns.scatterplot(data=sample, x="unit_price", y="revenue", hue="quantity",
                palette="viridis", alpha=0.6)
plt.title("Unit Price vs Order Value (5,000-row sample)")
save_fig("14_price_vs_revenue.png")

# ----------------------------------------------------------------------
# STEP 13: CUSTOMER PURCHASING BEHAVIOUR
# ----------------------------------------------------------------------
header("STEP 13: CUSTOMER BEHAVIOUR")
repeat_rate = (cust["orders"] > 1).mean() * 100
top20_n = int(len(cust) * 0.2)
share_top20 = cust.nlargest(top20_n, "total_spent")["total_spent"].sum() / cust["total_spent"].sum() * 100
print(f"Total customers: {len(cust):,}")
print(f"Repeat customers (>1 order): {repeat_rate:.1f}%")
print(f"Average orders per customer: {cust['orders'].mean():.2f}")
print(f"Average lifetime spend:      {cust['total_spent'].mean():,.2f}")
print(f"Churn rate (customers):      {cust['churn'].mean()*100:.1f}%")
print(f"Top 20% of customers generate {share_top20:.1f}% of revenue")
print("\nTop 10 customers by spend:\n",
      cust.nlargest(10, "total_spent")[["customer_id", "orders", "total_spent"]].to_string(index=False))

known = df[df["returns_known"]]
print(f"\nOverall return rate (known rows): {known['returns'].mean()*100:.1f}%")
print("Churn rate by gender (%):\n", (cust.groupby("gender")["churn"].mean() * 100).round(2).to_string())
print("\nChurned vs active customers - average spend:\n",
      cust.groupby("churn")[["total_spent", "orders"]].mean().round(2).to_string())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.countplot(x=cust["orders"].clip(upper=10), ax=axes[0], color="#21918c")
axes[0].set_title("Orders per Customer (10 = 10 or more)")
sns.scatterplot(data=cust.sample(min(5000, len(cust)), random_state=1),
                x="orders", y="total_spent", alpha=0.4, ax=axes[1], color="#440154")
axes[1].set_title("Orders vs Total Spend per Customer (sample)")
save_fig("15_customer_behaviour.png")

day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
fig, axes = plt.subplots(1, 3, figsize=(17, 5))
wd = df.groupby("weekday")["revenue"].sum().reindex(day_order)
sns.barplot(x=wd.index, y=wd.values, ax=axes[0], color="#5ec962")
axes[0].set_title("Revenue by Day of Week"); axes[0].tick_params(axis="x", rotation=40)
hr = df.groupby("hour")["revenue"].sum()
sns.barplot(x=hr.index, y=hr.values, ax=axes[1], color="#31688e")
axes[1].set_title("Revenue by Hour of Day")
pm = df.groupby("payment_method")["revenue"].sum().sort_values(ascending=False)
sns.barplot(x=pm.index, y=pm.values, ax=axes[2], color="#fde725")
axes[2].set_title("Revenue by Payment Method")
save_fig("16_time_and_payment_patterns.png")

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
cr = known.groupby("category")["returns"].mean() * 100
sns.barplot(x=cr.index, y=cr.values, ax=axes[0], color="#3b528b")
axes[0].set_title("Return Rate (%) by Category")
ch = (cust.groupby("gender")["churn"].mean() * 100)
sns.barplot(x=ch.index, y=ch.values, ax=axes[1], color="#35b779")
axes[1].set_title("Churn Rate (%) by Gender")
save_fig("17_returns_and_churn.png")

# ----------------------------------------------------------------------
# STEP 14: KEY INSIGHTS SUMMARY
# ----------------------------------------------------------------------
header("KEY INSIGHTS")
best_month = monthly.idxmax()
best_cat = cat.index[0]
print(f"1. Total revenue: {df['revenue'].sum():,.0f} from {len(df):,} purchases by {len(cust):,} customers.")
print(f"2. Peak month: {best_month} ({monthly.max():,.0f}); best quarter: {quarterly.idxmax()}.")
print(f"3. Top category by revenue: {best_cat} ({cat['share_of_revenue_%'].iloc[0]:.1f}% of sales).")
print(f"4. Highest average order value category: {cat['avg_order_value'].idxmax()}; "
      f"highest return rate: {cat['return_rate_%'].idxmax()}.")
print(f"5. Average order value: {aov:,.0f}.")
print(f"6. Biggest-spending age group: {age_tbl['sum'].idxmax()}.")
print(f"7. Repeat-customer rate: {repeat_rate:.1f}%; top 20% customers = {share_top20:.1f}% of revenue.")
print(f"8. Churn rate: {cust['churn'].mean()*100:.1f}%; overall return rate: {known['returns'].mean()*100:.1f}%.")

df.drop(columns=["customer_name"]).to_csv("cleaned_ecommerce_data.csv", index=False)
print(f"\nDone. {len(os.listdir(FIG_DIR))} charts saved in '{FIG_DIR}/' and cleaned data saved to cleaned_ecommerce_data.csv")