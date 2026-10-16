import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# ------------------------------------------------------------------ CONFIG
DATA_PATH = "Reviews.csv"
MAX_ROWS = 20000                             # random sample size for big files (None = use everything)
OUT_DIR = "sentiment_outputs"
POS_THRESHOLD, NEG_THRESHOLD = 0.05, -0.05   # standard VADER cut-offs
MAX_EMOTION_ROWS = 3000                      # NRC scoring is slow, so sample large datasets

COLS = {                       # set for the Kaggle "Amazon Fine Food Reviews" Reviews.csv
    "text": "Text",            # required
    "rating": "Score",         # 1-5 stars, optional
    "date": "Time",            # optional, enables the trend chart (Unix timestamps are handled)
}
# ---------------------------------------------------------------------------

os.makedirs(OUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")
COLORS = {"Positive": "#2a9d8f", "Neutral": "#6c757d", "Negative": "#e76f51"}
EMOTIONS = ["joy", "trust", "anticipation", "surprise", "fear", "sadness", "disgust", "anger"]

try:
    from nrclex import NRCLex
    HAS_NRC = True
except Exception:
    HAS_NRC = False


def make_demo_data(n=400, seed=7):
    rng = np.random.default_rng(seed)
    pos = ["Absolutely love this product, works perfectly and arrived fast!",
           "Great quality and excellent value. Highly recommend.",
           "Fantastic battery life, I am very happy with this purchase.",
           "Beautiful design and super easy to use. Five stars!",
           "Amazing sound, comfortable fit, and the delivery was quick."]
    neu = ["It is okay, does the job but nothing special.",
           "Arrived on time. Average quality for the price.",
           "The product is fine, I have not used it much yet.",
           "Works as described. Packaging was standard."]
    neg = ["Terrible quality, it broke after two days. Very disappointed.",
           "Worst purchase ever, a complete waste of money.",
           "Battery drains fast and customer support was awful.",
           "Poor build, arrived damaged and the seller ignored me.",
           "I hate it. Stopped working and I am angry about the refund delay."]
    texts, ratings = [], []
    for _ in range(n):
        kind = rng.choice(["pos", "neu", "neg"], p=[0.55, 0.15, 0.30])
        pool, r = {"pos": (pos, [4, 5]), "neu": (neu, [3]), "neg": (neg, [1, 2])}[kind]
        texts.append(rng.choice(pool))
        ratings.append(int(rng.choice(r)))
    dates = pd.to_datetime("2025-01-01") + pd.to_timedelta(rng.integers(0, 365, n), unit="D")
    return pd.DataFrame({"review_text": texts, "rating": ratings, "review_date": dates})


# ------------------------------------------------------------------ LOAD & CLEAN
DEMO = not os.path.exists(DATA_PATH)
if not DEMO:
    df = pd.read_csv(DATA_PATH)
    print(f"Loaded {len(df):,} rows from {DATA_PATH}")
else:
    print(f"'{DATA_PATH}' not found - using generated demo data.")
    df = make_demo_data()
    COLS = {"text": "review_text", "rating": "rating", "date": "review_date"}

T = COLS["text"]
R = COLS["rating"] if COLS.get("rating") in df.columns else None
D = COLS["date"] if COLS.get("date") in df.columns else None

df = df.dropna(subset=[T]).copy()
if not DEMO:
    df = df.drop_duplicates(subset=[T])
df[T] = df[T].astype(str).str.strip()
df = df[df[T].str.len() > 0]
if MAX_ROWS and len(df) > MAX_ROWS:
    df = df.sample(MAX_ROWS, random_state=42)
    print(f"Using a random sample of {MAX_ROWS:,} rows")
if D:
    if pd.api.types.is_numeric_dtype(df[D]):
        df[D] = pd.to_datetime(df[D], unit="s", errors="coerce")   # Unix timestamp
    else:
        df[D] = pd.to_datetime(df[D], errors="coerce")
print(f"{len(df):,} usable texts after cleaning\n")

# ------------------------------------------------------------------ SENTIMENT (VADER)
analyzer = SentimentIntensityAnalyzer()
df["compound"] = df[T].apply(lambda t: analyzer.polarity_scores(t)["compound"])
df["sentiment"] = np.select(
    [df["compound"] >= POS_THRESHOLD, df["compound"] <= NEG_THRESHOLD],
    ["Positive", "Negative"], default="Neutral")

dist = df["sentiment"].value_counts().reindex(["Positive", "Neutral", "Negative"]).fillna(0).astype(int)
pct = (dist / dist.sum() * 100).round(1)
print("=== SENTIMENT DISTRIBUTION ===")
print(pd.DataFrame({"count": dist, "pct": pct}), "\n")

# ------------------------------------------------------------------ RATING AGREEMENT
agreement = None
if R:
    df[R] = pd.to_numeric(df[R], errors="coerce")
    stars = np.select([df[R] >= 4, df[R] <= 2], ["Positive", "Negative"], default="Neutral")
    stars = np.where(df[R].isna(), None, stars)
    valid = df[R].notna()
    agreement = (df.loc[valid, "sentiment"].values == stars[valid]).mean() * 100
    print(f"Text sentiment agrees with star rating in {agreement:.1f}% of reviews\n")

# ------------------------------------------------------------------ TOP WORDS
EXTRA_STOP = ["did", "don", "didn", "doesn", "isn", "wasn", "just", "really", "product", "like", "ve", "ll"]
vec = CountVectorizer(stop_words=list(ENGLISH_STOP_WORDS) + EXTRA_STOP, min_df=2, token_pattern=r"(?u)\b[a-zA-Z]{3,}\b")
top_pos = top_neg = None
try:
    X = vec.fit_transform(df[T].str.lower())
    vocab = np.array(vec.get_feature_names_out())
    pos_m, neg_m = (df["sentiment"] == "Positive").values, (df["sentiment"] == "Negative").values
    if pos_m.sum() and neg_m.sum():
        pos_f = np.asarray(X[pos_m].sum(axis=0)).ravel() / pos_m.sum()
        neg_f = np.asarray(X[neg_m].sum(axis=0)).ravel() / neg_m.sum()
        diff = pos_f - neg_f
        hi, lo = np.argsort(diff)[::-1][:10], np.argsort(diff)[:10]
        hi, lo = hi[diff[hi] > 0], lo[diff[lo] < 0]          # keep only words that lean the right way
        if len(hi):
            top_pos = pd.Series(diff[hi], index=vocab[hi])
            print("Words most tied to POSITIVE:", ", ".join(top_pos.index))
        if len(lo):
            top_neg = pd.Series(-diff[lo], index=vocab[lo])
            print("Words most tied to NEGATIVE:", ", ".join(top_neg.index))
        print()
except ValueError:
    print("Not enough text to extract keywords.\n")

# ------------------------------------------------------------------ EMOTIONS (NRC)
def emotion_scores(text):
    """Return {emotion: count}. Handles both the old (3.x) and new (4.x) NRCLex interfaces."""
    try:
        return NRCLex(text).raw_emotion_scores        # nrclex 3.x
    except (AttributeError, TypeError):
        obj = NRCLex()                                # nrclex 4.x
        obj.load_raw_text(text)
        return obj.raw_emotion_scores


emotions = None
if HAS_NRC:
    try:
        sample = df[T].sample(min(len(df), MAX_EMOTION_ROWS), random_state=1)
        totals = pd.Series(0.0, index=EMOTIONS)
        print(f"Scoring emotions for {len(sample):,} texts (this can take a few minutes)...")
        for text in sample:
            scores = emotion_scores(text)
            for e in EMOTIONS:
                totals[e] += scores.get(e, 0)
        if totals.sum() > 0:
            emotions = (totals / totals.sum() * 100).round(1)
            print("=== EMOTION SHARE (%) ===")
            print(emotions.sort_values(ascending=False), "\n")
    except Exception as e:
        print(f"Emotion detection skipped ({e}).")
        print("Try: python -m pip install nrclex==3.0.0   then run again.\n")
else:
    print("NRCLex not installed - skipping emotions. Run: pip install nrclex\n")

# ------------------------------------------------------------------ TREND
trend = None
if D and df[D].notna().any():
    tmp = df.dropna(subset=[D]).copy()
    tmp["month"] = tmp[D].dt.to_period("M").dt.to_timestamp()
    trend = pd.crosstab(tmp["month"], tmp["sentiment"], normalize="index") * 100
    trend = trend.reindex(columns=["Positive", "Neutral", "Negative"]).fillna(0)

# ------------------------------------------------------------------ DASHBOARD
fig = plt.figure(figsize=(18, 10))
gs = GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.3)
fig.suptitle("Sentiment Analysis Dashboard", fontsize=22, fontweight="bold", x=0.06, ha="left", color="#1f3a5f")


def na(ax, title):
    ax.set_title(title, loc="left", fontweight="bold")
    ax.text(0.5, 0.5, "not available", ha="center", va="center", color="grey", transform=ax.transAxes)
    ax.set_xticks([]); ax.set_yticks([])


ax = fig.add_subplot(gs[0, 0])
ax.bar(dist.index, dist.values, color=[COLORS[k] for k in dist.index])
for i, (v, p) in enumerate(zip(dist.values, pct.values)):
    ax.text(i, v, f"{p}%", ha="center", va="bottom", fontweight="bold")
ax.set_title("Sentiment distribution", loc="left", fontweight="bold")

ax = fig.add_subplot(gs[0, 1])
if R:
    sns.boxplot(data=df.dropna(subset=[R]), x=R, y="compound", color="#9fb8d0", ax=ax)
    ax.set_title("Sentiment score by star rating", loc="left", fontweight="bold")
else:
    sns.histplot(df["compound"], bins=30, color="#1f3a5f", ax=ax)
    ax.set_title("Sentiment score distribution", loc="left", fontweight="bold")

ax = fig.add_subplot(gs[0, 2])
if trend is not None and len(trend) > 1:
    for k in ["Positive", "Neutral", "Negative"]:
        ax.plot(trend.index, trend[k], marker="o", color=COLORS[k], label=k, lw=2)
    ax.legend(frameon=False)
    ax.set_ylabel("% of texts")
    ax.set_title("Sentiment trend over time", loc="left", fontweight="bold")
    plt.setp(ax.get_xticklabels(), rotation=30)
else:
    na(ax, "Sentiment trend over time")

ax = fig.add_subplot(gs[1, 0])
if top_pos is not None:
    top_pos.sort_values().plot(kind="barh", color=COLORS["Positive"], ax=ax)
    ax.set_title("Words tied to positive text", loc="left", fontweight="bold")
else:
    na(ax, "Words tied to positive text")

ax = fig.add_subplot(gs[1, 1])
if top_neg is not None:
    top_neg.sort_values().plot(kind="barh", color=COLORS["Negative"], ax=ax)
    ax.set_title("Words tied to negative text", loc="left", fontweight="bold")
else:
    na(ax, "Words tied to negative text")

ax = fig.add_subplot(gs[1, 2])
if emotions is not None:
    emotions.sort_values().plot(kind="barh", color="#1f3a5f", ax=ax)
    ax.set_xlabel("% of emotion words")
    ax.set_title("Emotions detected (NRC lexicon)", loc="left", fontweight="bold")
else:
    na(ax, "Emotions detected (NRC lexicon)")

fig.savefig(os.path.join(OUT_DIR, "sentiment_dashboard.png"), dpi=150, bbox_inches="tight")
plt.close(fig)

# ------------------------------------------------------------------ SAVE DATA + INSIGHTS
df.to_csv(os.path.join(OUT_DIR, "scored_data.csv"), index=False)

L = ["# Key Insights", "", "## Findings", ""]
L.append(f"- Analysed **{len(df):,}** texts: **{pct['Positive']}%** positive, "
         f"**{pct['Neutral']}%** neutral, **{pct['Negative']}%** negative "
         f"(average score {df['compound'].mean():+.2f}).")
if agreement is not None:
    L.append(f"- Text sentiment matches the star rating **{agreement:.0f}%** of the time.")
if top_neg is not None:
    L.append(f"- Negative text is dominated by: **{', '.join(top_neg.index[:5])}**.")
if top_pos is not None:
    L.append(f"- Positive text is dominated by: **{', '.join(top_pos.index[:5])}**.")
if emotions is not None:
    L.append(f"- Strongest emotions: **{', '.join(emotions.sort_values(ascending=False).index[:3])}**.")
if trend is not None and len(trend) >= 4:
    half = len(trend) // 2
    shift = trend["Positive"].iloc[half:].mean() - trend["Positive"].iloc[:half].mean()
    L.append(f"- Positive share moved **{shift:+.1f} percentage points** between the first and second half of the period.")

L += ["", "## Recommendations", ""]
if top_neg is not None:
    L.append(f"- Investigate the issues behind negative terms ({', '.join(top_neg.index[:3])}) and track them in product and support reviews.")
if top_pos is not None:
    L.append(f"- Use positive themes ({', '.join(top_pos.index[:3])}) in marketing messages and product pages.")
L.append("- Respond quickly to negative texts to recover unhappy customers.")
L.append("- Re-run this analysis monthly to catch sentiment shifts early.")
with open(os.path.join(OUT_DIR, "key_insights.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(L))

print("\n".join(L))
print(f"\nSaved outputs to ./{OUT_DIR}/")