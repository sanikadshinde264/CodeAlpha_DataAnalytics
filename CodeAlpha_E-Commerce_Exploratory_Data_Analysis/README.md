# 🛒 CodeAlpha E-Commerce Exploratory Data Analysis (EDA)

📊 Exploratory Data Analysis of an e-commerce sales and customer dataset — completed as part of the **CodeAlpha Data Analytics Internship (Task 2)**.

## 📂 Dataset

📄 **File:** `ecommerce_customer_data_custom_ratios.csv`

📌 **Source:** Kaggle

- 🛍️ Total Purchases: 250,000
- 👥 Total Customers: 49,673
- 📅 Date Range: January 2020 – September 2023
- 📊 Features: Customer ID, Purchase Date, Product Category, Product Price, Quantity, Total Purchase Amount, Payment Method, Customer Age, Returns, Customer Name, Age, Gender, Churn

🔗 **Dataset Link:** [Add Kaggle Dataset URL Here]

⚠️ The CSV file is not included in this repository. Download it from Kaggle and place it inside the `data/` folder.

## 🛠️ Tools & Technologies

- 🐍 Python
- 🐼 Pandas
- 🔢 NumPy
- 📈 Matplotlib
- 🎨 Seaborn
- 🧪 SciPy

## 🔍 Analysis Performed

- 📋 Data structure, data types, and summary statistics
- 🧹 Missing values, duplicates, duplicate Age column, and revenue consistency checks
- 📦 Outlier detection using the IQR method and boxplots
- 📅 Monthly, quarterly, and yearly sales trends and seasonality
- 🛍️ Revenue and units sold by product category and price band
- 📊 Category comparison: revenue, average order value, and return rate
- 👥 Customer age and gender spending patterns
- 💰 Average order value and statistical hypothesis testing
- 🔗 Correlation analysis between numerical variables
- 🛒 Customer behavior: repeat purchases, top customers, churn, returns, time, and payment patterns

## ⚙️ How to Run

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/CodeAlpha_ECommerce_EDA.git
cd CodeAlpha_ECommerce_EDA
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add the Dataset

Download the Kaggle dataset and place the CSV file inside the `data/` directory.

### 4️⃣ Run the Analysis

```bash
python eda_ecommerce.py
```

📁 **Output:**
- 📊 Charts are saved in the `figures/` directory.
- 🧹 Cleaned data is saved as `cleaned_ecommerce_data.csv`.

## 📈 Key Insights

### 1. 🛍️ Dataset Overview
Analyzed **250,000 purchases** made by **49,673 customers**, generating approximately **681 million** in recorded purchase value.

### 2. 🧹 Data Quality
- `Returns` has missing values in approximately 19% of rows.
- `Age` duplicates `Customer Age`.
- `Total Purchase Amount` never equals `Product Price × Quantity`.
- No duplicate rows, missing purchase dates, or detected outliers.

### 3. 📅 Sales Trends
Quarterly revenue remains relatively stable at around 45–47 million, with no strong seasonality. The lower value in Q3 2023 is due to incomplete data ending on September 15, 2023.

### 4. 🏷️ Product Category Performance
Books and Clothing each contribute approximately 30% of revenue, while Electronics and Home contribute around 20% each.

Average order value is nearly identical across categories, ranging from 2,714 to 2,736.

### 5. 👥 Customer Age Analysis
Average order value increases slightly with age, from 2,616 for customers aged 18–24 to 2,845 for those aged 65–70.

The correlation between age and revenue is weak (**0.05**).

### 6. ⚧️ Gender-Based Spending
The Mann–Whitney U test found no statistically significant difference in order value between men and women (**p = 0.47**).

### 7. 🔁 Customer Loyalty
- 96.6% of customers made more than one purchase.
- Customers made approximately 5 purchases on average.
- The top 20% of customers generated 35% of revenue.

### 8. ↩️ Returns & Customer Churn
- Approximately 50% of purchases with known return status were returned.
- Return rates were similar across categories.
- Customer churn is approximately 20%.
- Churned and active customers have similar spending levels.

### 9. 🔗 Correlation Analysis
Numerical variables show very weak correlations, suggesting that the dataset may be synthetic.

## 💡 Business Recommendation

🎯 **Investigate the high return rate.**

With approximately 50% of purchases with known return status marked as returned, analyzing return reasons, product quality, and customer feedback should be a priority.

## 🖼️ Visualizations

| 📊 Visualization | 🔗 Link |
|---|---|
| 📅 Monthly Revenue Trend | [View Chart](figures/03_monthly_sales_trend.png) |
| 🏷️ Category Analysis | [View Chart](figures/07_category_analysis.png) |
| 👥 Age & Gender Spending | [View Chart](figures/09_age_gender_spending.png) |
| 🔗 Correlation Heatmap | [View Chart](figures/13_correlation_heatmap.png) |

## ⚠️ Limitations

- 📦 No product names, order IDs, or cost column are available, so profit could not be calculated.
- 💰 `Total Purchase Amount` does not equal `Product Price × Quantity`; therefore, the recorded total was used as revenue.
- 🧪 The dataset appears synthetic, with many variables distributed relatively evenly.
- ↩️ Return-rate calculations exclude records with unknown return status.

## 👩‍💻 Author

**Sanika Deepak Shinde**

🎓 Data Analytics | Python | SQL | Power BI

🔗 [GitHub Profile](https://github.com/sanikadshinde264)

---

⭐ If you find this project useful, consider giving the repository a star!

📌 *Part of the CodeAlpha Data Analytics Internship — Task 2: Exploratory Data Analysis.*