# Scrapy Unleashed

Companion repository for Ahmed Elfakharany's Udemy course **Scrapy Unleashed** (course id 4602824).

Phase 1 scrapes [Books to Scrape](https://books.toscrape.com/), a stable sandbox catalogue. `archive/real_estate` is the retired Arizona project; that site blocks bots, so new lessons do not use it.

## Setup

Python 3.12.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows, activate with `.venv\Scripts\activate`.

`requirements.txt` pins Scrapy 2.13.x, itemloaders, and itemadapter. Splash and Playwright are not part of this phase.

## Run the starter spider

From the repository root:

```bash
python spider.py
```

The command prints a JSON list of the 20 books on the first catalogue page. Each object has `title`, `price`, and `availability`. A successful run is never `[]`.

```json
[
    {
        "title": "A Light in the Attic",
        "price": "£51.77",
        "availability": "In stock"
    }
]
```

## Run the Books to Scrape project

`projects/books_toscrape` is a Scrapy project with a `BookItem`, an Item Loader (input and output processors), and a CrawlSpider that follows `//li[@class="next"]/a` across the catalogue.

```bash
cd projects/books_toscrape
scrapy crawl books -O books.json
```

The project settings wait 1 second between requests. A full crawl covers all 50 pages (1000 books) and takes about a minute. Each item looks like this:

```json
{
    "title": "A Light in the Attic",
    "price": "51.77",
    "availability": "In stock",
    "rating": 3,
    "url": "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
}
```

To check pagination without downloading the whole catalogue, stop after the first two pages (20 books each):

```bash
scrapy crawl books -s CLOSESPIDER_ITEMCOUNT=40 -O books.json
```

That yields 40 books: 20 from https://books.toscrape.com/ and 20 from https://books.toscrape.com/catalogue/page-2.html. Page 2 starts with "In Her Wake". `CLOSESPIDER_PAGECOUNT` also counts the robots.txt request, so use the item count above when you want exactly two catalogue pages.
