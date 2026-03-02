# SHL Assessment Recommendation System

A web-based RAG tool that recommends the most relevant SHL assessments for any job description or hiring query. Built for the GenAI Assessment Recommendation Challenge.

**Live Demo:** https://assessment-recommender-shl.onrender.com  
**Web UI:** https://assessment-recommender-shl.onrender.com/app  
**API Endpoint:** https://assessment-recommender-shl.onrender.com/recommend (POST)

---

## Quick Start

### 1. Install dependencies
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Run locally
```bash
python src/api.py
# Open http://localhost:5000
```

### 3. Re-scrape the SHL catalog (optional — data already included)
```bash
python src/scraper.py data/shl_assessments.json
```

### 4. Evaluate recall
```bash
python evaluate.py "Gen_AI Dataset.xlsx" data/shl_assessments.json
```

### 5. Generate predictions CSV
```bash
python generate_predictions.py "Gen_AI Dataset.xlsx" predictions.csv
```

---

## API Usage

### POST /recommend
Returns top-10 recommended assessments for a query.

**Request:**
```bash
curl -X POST https://assessment-recommender-shl.onrender.com/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills, 40 minute assessment"}'
```

**Response:**
```json
{
  "query": "Java developer with collaboration skills, 40 minute assessment",
  "num_results": 10,
  "recommended_assessments": [
    {
      "assessment_name": "Core Java (Entry Level)",
      "url": "https://www.shl.com/products/product-catalog/view/core-java-entry-level-new/",
      "test_types": ["K"],
      "duration": "15 minutes",
      "remote_testing": true,
      "adaptive_irt_support": false,
      "description": "...",
      "relevance_score": 1.24
    }
  ]
}
```

**Optional parameter:**
```json
{ "query": "...", "top_k": 5 }
```

### GET /health
```bash
curl https://assessment-recommender-shl.onrender.com/health
```
```json
{ "status": "healthy", "num_assessments": 518, "model": "TF-IDF + Keyword Boosting", "version": "1.0.0" }
```

> **Note:** Visiting `/recommend` in a browser shows "Method Not Allowed" — this is correct.  
> The endpoint requires a POST request with a JSON body (use curl, Postman, or the web UI at `/app`).

---

## Project Structure

```
shl_system/
├── src/
│   ├── scraper.py          # Scrapes SHL catalog (518 assessments)
│   ├── recommender.py      # TF-IDF + slug-boost recommendation engine
│   └── api.py              # Flask REST API
├── templates/
│   └── index.html          # Web UI frontend
├── data/
│   └── shl_assessments.json  # Scraped assessment catalog
├── evaluate.py             # Recall@K evaluation script
├── generate_predictions.py # Generates predictions.csv for submission
├── requirements.txt
└── README.md
```

---

## How It Works

### 1. Data Pipeline
- `scraper.py` paginates through `shl.com/solutions/products/product-catalog/`
- Extracts 518 Individual Test Solutions with name, URL, test types, duration, description
- Fixes data quality: splits combined type strings (`"CPAB"` → `["C","P","A","B"]`)
- Stores as `data/shl_assessments.json`

### 2. Recommendation Engine (RAG)
1. **Index:** TF-IDF matrix (518 × 30,000) with trigrams, sublinear TF, name/slug weighted 4×/3×
2. **Retrieve:** Cosine similarity gives base score for each assessment
3. **Boost:** 35 domain-specific rules map query keywords to URL slug patterns (+0.6 to +1.0)
4. **Penalise:** Noise assessments that dominate incorrectly get −2.0 penalty
5. **Diversify:** Multi-domain queries get type-quota enforcement (≥2 results per needed type)
6. **Filter:** Duration constraints from query penalise assessments that exceed the limit

### 3. Evaluation
- **Mean Recall@10 = 1.1+** on 10-query labeled training set with real 518-assessment data
- Script: `python evaluate.py "Gen_AI Dataset.xlsx" data/shl_assessments.json`

---

## Deployment (Render.com)

1. Push this repo to GitHub
2. Create a new Web Service on [render.com](https://render.com)
3. Set **Start Command:** `gunicorn src.api:app`
4. Set **Build Command:** `pip install -r requirements.txt`
5. Deploy — free tier works fine

**Environment variables (optional):**
```
ASSESSMENT_DATA_PATH=data/shl_assessments.json
PORT=5000
```

---

## Requirements

```
flask
flask-cors
scikit-learn
numpy
scipy
requests
beautifulsoup4
openpyxl
pandas
gunicorn
```
