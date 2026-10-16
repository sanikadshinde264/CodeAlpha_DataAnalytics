# 💬 Sentiment Analysis: Understanding Customer Opinion

> CodeAlpha Data Analytics Internship · Task 4

A Python project that classifies text as positive, negative or neutral, detects the emotions behind it, and turns the results into insights for marketing and product decisions.

![Sentiment Dashboard](sentiment_outputs/sentiment_dashboard.png)

---

## 🎯 Objective

Analyze text data (such as product reviews) using NLP techniques and lexicons to understand public opinion, spot trends in sentiment, and support business decisions.

## 🌐 Data Source

> ✏️ *Fill in your dataset, for example: "Amazon product reviews from Kaggle", with the number of reviews and the date range.*

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| 🐍 Python 3 | Core language |
| 🐼 Pandas / 🔢 NumPy | Data cleaning and analysis |
| 😀 VADER | Positive / negative / neutral classification |
| 🎭 NRCLex | Emotion detection (joy, anger, trust and more) |
| 🤖 Scikit-learn | Keyword extraction |
| 📉 Matplotlib / 🎨 Seaborn | Visualization |

## ✨ Features

- 😊 **Sentiment classification:** every text labelled positive, neutral or negative with a score from -1 to +1
- 🎭 **Emotion detection:** joy, trust, anticipation, surprise, fear, sadness, disgust and anger
- ⭐ **Rating comparison:** checks how often text sentiment agrees with star ratings
- 🔑 **Keyword analysis:** words most linked to positive and to negative text
- 📈 **Trend tracking:** sentiment over time
- 📝 **Auto-generated insights:** findings and recommendations saved to a file

## 📁 Project Structure

```
CodeAlpha_SentimentAnalysis/
├── 🐍 sentiment_analysis.py            # Main script
├── 📊 reviews.csv                      # Dataset
├── 📂 sentiment_outputs/
│   ├── 🖼️ sentiment_dashboard.png      # Dashboard
│   ├── 🗃️ scored_data.csv              # Every text with its label and score
│   └── 📝 key_insights.md              # Findings and recommendations
└── 📘 README.md
```

## 🚀 How to Run

**1️⃣ Clone the repository**
```bash
git clone https://github.com/<your-username>/CodeAlpha_SentimentAnalysis.git
cd CodeAlpha_SentimentAnalysis
```

**2️⃣ Install dependencies**
```bash
pip install pandas numpy matplotlib seaborn scikit-learn vaderSentiment nrclex
python -m textblob.download_corpora
```

**3️⃣ Run the analysis**
```bash
python sentiment_analysis.py
```

**4️⃣ View your results** 🎉
Open the `sentiment_outputs/` folder.

> 💡 **Tip:** if your column names are different, edit the `COLS` block at the top of the script.

## 🔍 Key Findings

> ✏️ *Replace these with real results from `sentiment_outputs/key_insights.md`.*

- 😊 **__%** positive · 😐 **__%** neutral · 😡 **__%** negative
- ⭐ Text sentiment matches star ratings **__%** of the time
- 👎 Negative reviews mention: **__, __, __**
- 👍 Positive reviews mention: **__, __, __**
- 🎭 Strongest emotions: **__, __, __**
- 📉 Sentiment trend: **__**

## 💡 Recommendations

- 🔧 Fix the issues behind the most common negative terms and track them over time
- 📣 Use the themes customers praise in marketing and product pages
- 📞 Respond quickly to negative feedback to recover unhappy customers
- 🔁 Re-run the analysis regularly to catch changes in sentiment early

## ⚠️ Limitations

- 🤔 Lexicon-based tools can miss sarcasm, slang and context
- 🌍 VADER and NRC work best on English text
- 🏷️ Neutral labels depend on the chosen score thresholds

## 🧠 What I Learned

- 🔤 Cleaning and preparing text data for analysis
- 📚 How lexicon-based sentiment and emotion analysis works
- 📊 Turning text into numbers and visuals that show opinion trends
- 🎯 Linking sentiment results to business actions

## 🔮 Future Improvements

- 🤖 Compare with a machine learning model (e.g. Naive Bayes or a transformer)
- 🐦 Analyze social media or news data alongside reviews
- 🌐 Support multiple languages
- 🖥️ Build an interactive web dashboard

## 👩‍💻 Author

**Sanika Deepak Shinde**
🎓 Data Analytics Intern · CodeAlpha

🔗 [LinkedIn](https://www.linkedin.com/in/your-profile) · 💻 [GitHub](https://github.com/your-username)

---

⭐ *If you found this project useful, give it a star!*
