# LinguaLens — AI Text Bias & Manipulation Detector

A full-stack AI web application that analyzes any text and detects
hidden sentiment, political bias, and manipulative language in real time.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange)

---

## What It Does

Paste any text — news headline, political speech, product review —
and get an instant breakdown of:

- **Sentiment** — Positive / Negative / Neutral with confidence score
- **Manipulation Level** — Low / Medium / High with trigger words highlighted
- **Political Bias** — Left-leaning / Right-leaning / Neutral
- **AI Verdict** — Plain English explanation of what was detected
- **Analysis History** — Last 10 analyses saved and displayed

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (vanilla) |
| Backend | FastAPI + Uvicorn |
| NLP Model | DistilBERT (HuggingFace Transformers) |
| Bias Detection | Keyword-based scoring |
| Manipulation Detection | Multi-category keyword scoring |
| History Storage | JSON file |

---

## Project Structure
```
lie-bias-detector/
├── backend/
│   ├── analyzer.py     # Core NLP logic — sentiment, bias, manipulation
│   ├── words.py        # Keyword dictionaries (100+ words)
│   └── main.py         # FastAPI server + API routes
├── frontend/
│   └── index.html      # Full UI — dark theme, animated results
├── results/
│   └── history.json    # Auto-saved analysis history
└── requirements.txt
```

---

## How to Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/YASHWARDHAN1011/lie-bias-detector.git
cd lie-bias-detector
```

**2. Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Start the server**
```bash
uvicorn backend.main:app --reload
```

**5. Open in browser**
```
http://127.0.0.1:8000
```

---

## Example Results

| Input | Sentiment | Manipulation | Bias |
|---|---|---|---|
| Political speech with loaded language | Negative | High | Right-leaning |
| Neutral news article | Neutral | Low | Neutral |
| Fake review with exaggerations | Positive | High | Neutral |
| Clickbait headline | Negative | High | Neutral |

---

## Limitations

- Bias detection is keyword-based — a prototype, not a perfect classifier
- Works best on English text
- Short texts may have lower confidence scores
- Fine-tuning on a labeled political dataset would improve bias accuracy

---

## Future Improvements

- Fine-tune RoBERTa on LIAR dataset for better bias detection
- Add multilingual support
- Add attention visualization to highlight suspicious sentences
- Deploy on Hugging Face Spaces
```

Save it.

---

**Step 3 — Update requirements.txt**

Open `requirements.txt` and paste:
```
fastapi
uvicorn
transformers
torch
pandas