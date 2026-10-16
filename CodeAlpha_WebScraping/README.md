# 🕷️ Web Scraping: E-commerce Product Analysis

> CodeAlpha Data Analytics Internship · Task 1

A Python web scraper that collects product data from a public e-commerce sandbox site and turns it into a clean, analysis-ready CSV dataset.

---

## 🎯 Objective

Use Python to extract data from web pages, handle HTML structure and pagination, and build a custom dataset for e-commerce product analysis.

## 🌐 Data Source

**[books.toscrape.com](https://books.toscrape.com)** is a public sandbox website built specifically for practising web scraping, so it is safe and legal to scrape.

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| 🐍 Python 3 | Core language |
| 🌍 Requests | Fetching web pages |
| 🍜 BeautifulSoup4 | Parsing HTML |
| 🐼 Pandas | Cleaning data and saving CSV |

## 📦 Data Collected

| Field | Description |
|-------|-------------|
| 📖 `title` | Product name |
| 💰 `price` | Price in £ (converted to a number) |
| ⭐ `rating` | Star rating, 1 to 5 |
| ✅ `in_stock` | Availability (True/False) |
| 🗂️ `category` | Product category |
| 🔢 `upc` | Unique product code |
| 💬 `num_reviews` | Number of reviews |
| 📦 `stock_count` | Units available |
| 🔗 `url` | Product page link |

## ✨ Features

- 🔄 **Automatic pagination:** follows the "next" button through every page
- 🔍 **Two-level scraping:** listing pages plus individual product pages
- 🔁 **Retry logic:** retries failed requests up to 3 times
- ⏱️ **Polite scraping:** 1-second delay between requests
- 🧹 **Data cleaning:** removes duplicates, fixes encoding, converts prices and ratings to numbers
- 💾 **CSV export:** saves a ready-to-analyse `products.csv`

## 📁 Project Structure

```
CodeAlpha_WebScraping/
├── 🐍 scrape_products.py   # Main scraper script
├── 📊 products.csv         # Generated dataset
└── 📘 README.md            # Project documentation
```

## 🚀 How to Run

**1️⃣ Clone the repository**
```bash
git clone https://github.com/<your-username>/CodeAlpha_WebScraping.git
cd CodeAlpha_WebScraping
```

**2️⃣ Install dependencies**
```bash
pip install requests beautifulsoup4 pandas
```

**3️⃣ Run the scraper**
```bash
python scrape_products.py
```

**4️⃣ Get your data** 🎉
The scraper creates `products.csv` in the same folder.

> 💡 **Tip:** to test quickly, set `MAX_PAGES = 2` in the script. For a faster full run, set `SCRAPE_DETAILS = False`.

## 📈 Key Insights

> ✏️ *Fill these in after running the scraper and exploring `products.csv`.*

- 💷 Average product price: **£__**
- ⭐ Average rating: **__ / 5**
- 🏆 Most expensive category: **__**
- 📚 Category with the most products: **__**
- 🔗 Relationship between price and rating: **__**

## 🧠 What I Learned

- 🧱 Reading and navigating HTML structure with CSS selectors
- 🔄 Handling pagination and multi-page navigation
- 🛡️ Writing reliable scrapers with error handling and delays
- 🧹 Turning messy web data into a clean, structured dataset
- ⚖️ Scraping ethically: checking `robots.txt` and site terms

## 🔮 Future Improvements

- 📊 Add visualizations and a full EDA notebook
- 🗄️ Store data in a database (SQLite)
- ⚡ Speed up scraping with concurrent requests
- 🧭 Extend to other e-commerce sites

## 👩‍💻 Author

**Sanika Deepak Shinde**
🎓 Data Analytics Intern · CodeAlpha

🔗 [LinkedIn](https://www.linkedin.com/in/your-profile) · 💻 [GitHub](https://github.com/your-username)

---

⭐ *If you found this project useful, give it a star!*
