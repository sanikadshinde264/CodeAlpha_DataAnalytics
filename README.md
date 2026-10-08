# CodeAlpha_ECommerce_EDA

Exploratory Data Analysis of an e-commerce sales and customer dataset - CodeAlpha Data Analytics Internship (Task 2).

## Dataset
`ecommerce_customer_data_custom_ratios.csv` (Kaggle) - 250,000 purchases, 2020-2023.
Columns: Customer ID, Purchase Date, Product Category, Product Price, Quantity, Total Purchase Amount,
Payment Method, Customer Age, Returns, Customer Name, Age, Gender, Churn.

## Tools
Python, Pandas, NumPy, Matplotlib, Seaborn, SciPy

## Analysis performed
- Data structure, data types, summary statistics
- Missing values (Returns), duplicates, duplicate Age column, Total vs Price x Quantity check
- Outlier detection (IQR method + boxplots)
- Monthly, quarterly and yearly sales trends, seasonality
- Revenue and units by category and price band
- Category comparison: revenue, average order value, return rate
- Customer age and gender patterns
- Average order value, with hypothesis tests (Mann-Whitney U, Kruskal-Wallis)
- Correlation between numerical variables
- Customer behaviour: repeat rate, top customers, churn, returns, time-of-day and payment patterns

## How to run
```bash
pip install -r requirements.txt
# place the CSV in the data/ folder
python eda_ecommerce.py
```
Charts are saved in `figures/`; the cleaned data is saved as `cleaned_ecommerce_data.csv`.

## Key Insights
(Write your 5-8 findings here, in your own words.)

## Limitations
- No product names, order IDs or cost column, so profit could not be calculated.
- Total Purchase Amount does not equal Price x Quantity, so the recorded total was used as revenue.
- The data appears synthetic: most variables are evenly distributed and show almost no correlation.

## Author
Sanika Deepak Shinde