import re
import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://books.toscrape.com/catalogue/"
START_URL = urljoin(BASE_URL, "page-1.html")
DELAY = 1.0              # seconds between requests (be polite)
SCRAPE_DETAILS = True    # also visit each product page for category, UPC, stock count
MAX_PAGES = None         # set e.g. 3 to test quickly

RATING_MAP = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0 (educational scraping project)"})


def get_soup(url):
    """Fetch a URL and return parsed HTML, retrying on failure."""
    for attempt in range(3):
        try:
            r = session.get(url, timeout=15)
            r.raise_for_status()
            r.encoding = "utf-8"  # avoids 'Â£' in prices
            return BeautifulSoup(r.text, "html.parser")
        except requests.RequestException as e:
            print(f"  retry {attempt + 1}/3 for {url}: {e}")
            time.sleep(2 * (attempt + 1))
    return None


def parse_listing(card, page_url):
    """Extract fields from one product card on a listing page."""
    link = card.h3.a
    price_text = card.select_one("p.price_color").get_text(strip=True)
    rating_word = card.select_one("p.star-rating")["class"][1]
    return {
        "title": link["title"],
        "price": float(re.sub(r"[^\d.]", "", price_text)),
        "rating": RATING_MAP.get(rating_word),
        "in_stock": "in stock" in card.select_one("p.availability").get_text().lower(),
        "url": urljoin(page_url, link["href"]),
    }


def parse_detail(url):
    """Extract extra fields from a product detail page."""
    soup = get_soup(url)
    if soup is None:
        return {}
    crumbs = soup.select("ul.breadcrumb li a")
    table = {row.th.get_text(strip=True): row.td.get_text(strip=True)
             for row in soup.select("table.table-striped tr")}
    stock_match = re.search(r"\((\d+) available\)", table.get("Availability", ""))
    return {
        "category": crumbs[-1].get_text(strip=True) if len(crumbs) >= 3 else None,
        "upc": table.get("UPC"),
        "num_reviews": int(table.get("Number of reviews", 0)),
        "stock_count": int(stock_match.group(1)) if stock_match else None,
    }


def main():
    rows, url, page = [], START_URL, 1
    while url and (MAX_PAGES is None or page <= MAX_PAGES):
        print(f"Scraping page {page}: {url}")
        soup = get_soup(url)
        if soup is None:
            break

        for card in soup.select("article.product_pod"):
            item = parse_listing(card, url)
            if SCRAPE_DETAILS:
                item.update(parse_detail(item["url"]))
                time.sleep(DELAY)
            rows.append(item)

        nxt = soup.select_one("li.next a")      # pagination: follow the "next" link
        url = urljoin(url, nxt["href"]) if nxt else None
        page += 1
        time.sleep(DELAY)

    df = pd.DataFrame(rows).drop_duplicates(subset="url")
    df.to_csv("products.csv", index=False)
    print(f"\nSaved {len(df)} products to products.csv")
    print(df.head())
    print("\nAverage price by rating:")
    print(df.groupby("rating")["price"].mean().round(2))


if __name__ == "__main__":
    main()
