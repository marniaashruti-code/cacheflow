# CacheFlow

CacheFlow shows how smart caching, deduplication, and compression can cut the storage costs and energy footprint of data-heavy systems — making essential digital tools (like telehealth platforms, school resource libraries, and crisis-response systems) more affordable for the communities that need them most.

## Live Demo
🔗 [Try CacheFlow live](https://cacheflow-zqju5wnuljzxa9c4ox2d8i.streamlit.app)

## What It Does
- **Deduplication** — detects identical files using SHA-256 hashing and stores only one copy
- **Compression** — shrinks file sizes using zlib compression
- **Smart Caching (LRU)** — a real Least Recently Used cache that keeps frequently accessed files fast and evicts the least-used ones
- **Real Savings Calculator** — converts storage saved into estimated dollar and energy savings, based on public AWS S3 pricing and data center energy-use estimates

## Why It Matters
High cloud storage costs are one reason essential digital tools stay out of reach for underserved communities and budget-constrained nonprofits. By cutting the resources needed to store and serve data, CacheFlow helps make those tools cheaper to run — while also shrinking the energy footprint behind them.

## Tech Stack
- Python
- Streamlit
- Standard library: `hashlib`, `zlib`, `collections.OrderedDict`

## Running Locally
git clone https://github.com/marniaashruti-code/cacheflow.git
cd cacheflow
pip install -r requirements.txt
streamlit run app.py
## Running Locally

```bash
git clone https://github.com/marniaashruti-code/cacheflow.git
cd cacheflow
pip install -r requirements.txt
streamlit run app.py
```

## Built For

Congressional App Challenge 2026
