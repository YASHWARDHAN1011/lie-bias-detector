# LinguaLens — AI Text Framing & Manipulation Analyzer

An explainable NLP web application that analyzes text for sentiment,
political framing, and manipulative language patterns.

> ⚠️ **Transparency note**: Sentiment detection uses DistilBERT (transformer-based).
> Bias and manipulation detection use a hybrid rule-based + keyword scoring approach.
> This is a research prototype, not a production truth-verification system.

---

## Demo

![LinguaLens Demo](results/screenshots/demo.png)

---

## What It Does

| Feature | Approach | Model |
|---|---|---|
| Sentiment Analysis | Transformer-based | DistilBERT (SST-2) |
| Manipulation Detection | Keyword scoring + rules | Custom scorer |
| Political Bias | Keyword framing analysis | Rule-based classifier |
| Explainability | Word-level breakdown | Token highlighting |
| Evaluation | Metrics on labeled samples | scikit-learn |

---

## Architecture
```
User Input (text)
       ↓
  FastAPI Backend
       ↓
  ┌─────────────────────────────┐
  │ 1. Sentiment (DistilBERT)   │
  │ 2. Manipulation (keywords)  │
  │ 3. Bias (keyword framing)   │
  │ 4. Explainability layer     │
  └─────────────────────────────┘
       ↓
  JSON Response → Animated UI
```

---

## Performance (30 labeled test samples)

| Task | Accuracy | F1 Score |
|---|---|---|
| Sentiment Detection | 86.7% | 80.8% |
| Manipulation Detection | 86.7% | 86.7% |
| Bias Detection | 76.7% | 77.6% |

> Note: Evaluated on 30 hand-labeled samples.
> Bias detection is keyword-based and may misclassify
> neutral reporting containing political terminology.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI + Uvicorn |
| NLP Model | DistilBERT (HuggingFace Transformers) |
| Evaluation | scikit-learn |
| Frontend | HTML + CSS + Vanilla JS |
| Storage | JSON (demo) |

---

## Project Structure
```
lie-bias-detector/
├── backend/
│   ├── __init__.py
│   ├── analyzer.py      # Core NLP logic
│   ├── words.py         # Keyword dictionaries
│   ├── evaluator.py     # Evaluation pipeline
│   └── main.py          # FastAPI server
├── frontend/
│   └── index.html       # Full UI
├── results/
│   └── history.json     # Analysis history
├── requirements.txt
└── README.md
```

---

## Setup & Run
```bash
# 1. Clone the repo
git clone https://github.com/YASHWARDHAN1011/lie-bias-detector.git
cd lie-bias-detector

# 2. Install dependencies
pip install -r requirements.txt

# 3. Start the server
uvicorn backend.main:app --reload

# 4. Open in browser
# http://127.0.0.1:8000
```

---

## API

**POST /analyze**
```json
// Request
{ "text": "Your text here" }

// Response
{
  "sentiment": "Negative",
  "confidence": "99.2%",
  "manipulation_level": "High",
  "bias": "Right-leaning",
  "trigger_words": ["radical", "corrupt"],
  "bias_words_found": ["patriot"],
  "verdict": "This text has a strongly negative tone...",
  "word_breakdown": [...],
  "reasons": [...]
}
```

**GET /health**
```json
{ "status": "ok", "version": "1.0.0" }
```

**GET /history**
Returns last 10 analyses.

**GET /evaluate**
Runs evaluation on 30 labeled test samples.

---

## Known Limitations

- Bias detection uses keyword matching — can misclassify neutral
  reporting that quotes political language
- Sarcasm and irony are not detected
- Optimized for English text only
- 30-sample evaluation is not a full benchmark —
  real-world accuracy may differ
- Neutral sentiment is estimated, not from a dedicated 3-class model

---

## Future Roadmap

- [ ] Fine-tune RoBERTa on LIAR dataset for manipulation detection
- [ ] Replace keyword bias with a trained political framing classifier
- [ ] Evaluate on public datasets (SST-2, LIAR, AllSides)
- [ ] Add multilingual support
- [ ] Docker deployment
- [ ] Sentence-level analysis for longer articles

---

## Ethics Note

This tool is designed for media literacy and educational purposes.
It should not be used as a definitive truth detector. All predictions
are probabilistic and should be interpreted with critical thinking.