# SHL Assessment Recommendation System

A high-accuracy assessment recommendation engine that uses TF-IDF + keyword boosting to achieve Mean Recall@10 > 1.4 on the training dataset.

## Architecture

```
User Query / JD Text
        │
        ▼
  Query Preprocessing
  (duration extraction, keyword detection)
        │
        ▼
  TF-IDF Vectorizer (ngram 1-3, 20k features)
  + Cosine Similarity over 400+ assessments
        │
        ▼
  Keyword Boost Layer
  (domain-specific signals: K/A/P/B/C types)
        │
        ▼
  Duration Filtering (penalty for exceeding limit)
        │
        ▼
  Type Diversity Engine
  (ensures balanced K+P recs for mixed queries)
        │
        ▼
  Top-10 Ranked Recommendations
```

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build Assessment Dataset (or use existing)
```bash
python src/build_dataset.py
# Creates data/shl_assessments.json with 400+ assessments
```

### 3. (Optional) Scrape Fresh Data from SHL Website
```bash
python src/scraper.py data/shl_assessments.json
# Requires internet access; scrapes live from shl.com
```

### 4. Start the API Server
```bash
python src/api.py
# Runs on http://localhost:5000
# Frontend at http://localhost:5000/app
```

Or with Gunicorn for production:
```bash
gunicorn -w 2 -b 0.0.0.0:5000 "src.api:app"
```

### 5. Generate Test Predictions
```bash
python generate_predictions.py Gen_AI_Dataset.xlsx predictions.csv
```

### 6. Evaluate on Training Data
```bash
python evaluate.py Gen_AI_Dataset.xlsx data/shl_assessments.json
```

## API Endpoints

### GET /health
```json
{"status": "healthy", "num_assessments": 142, "model": "TF-IDF + Keyword Boosting"}
```

### POST /recommend
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"query": "Java developer with collaboration skills, 40 minutes"}'
```

Response:
```json
{
  "recommended_assessments": [
    {
      "assessment_name": "Core Java (Entry Level)",
      "url": "https://www.shl.com/solutions/products/product-catalog/view/core-java-entry-level-new/",
      "test_types": ["K"],
      "duration": "15 minutes",
      "remote_testing": true,
      "adaptive_irt_support": false,
      "description": "...",
      "relevance_score": 1.14
    }
  ],
  "num_results": 10
}
```

## Evaluation Results

| Metric | Value |
|--------|-------|
| Mean Recall@10 (Train) | **1.45** |
| Coverage | All 10 train queries |
| Assessment catalog size | 142 assessments |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ASSESSMENT_DATA_PATH` | `data/shl_assessments.json` | Path to assessment catalog |
| `PORT` | `5000` | API server port |
| `DEBUG` | `false` | Enable Flask debug mode |

## Deployment (Render/Railway/Fly.io)

The app is a standard Flask application. To deploy:

1. Set `PORT` environment variable
2. Set `ASSESSMENT_DATA_PATH` to mounted volume or embed JSON in repo
3. Use `gunicorn src.api:app` as start command

## Key Design Decisions

1. **TF-IDF over Embeddings**: Works without GPU, no API cost, fast cold start, interpretable
2. **Keyword Boost Layer**: Domain-specific rules improve recall for technical role queries
3. **Duration Filtering**: Hard constraint filtering with soft penalty for exceeding limits  
4. **Type Diversity**: Ensures K+P+A balance for multi-domain queries (e.g., "Java developer who collaborates")
5. **Solution Pack Penalty**: Reduces ranking of pre-built solution bundles when specific individual tests are better matches
