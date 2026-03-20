try:
    from backend.real_evaluator import run_real_evaluation
    REAL_EVAL_AVAILABLE = True
except ImportError as e:
    print(f"Real evaluator not available: {e}")
    REAL_EVAL_AVAILABLE = False
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import sys
import logging
from datetime import datetime

# Fix imports — always use relative imports inside backend
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyzer import analyze_text
from evaluator import run_evaluation

# ── LOGGING ──────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s — %(levelname)s — %(message)s"
)
logger = logging.getLogger(__name__)

# ── APP ───────────────────────────────────────────────────────
app = FastAPI(
    title="LinguaLens API",
    description="AI-powered text bias and manipulation detector",
    version="1.0.0"
)

# ── CORS — restrict in production ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

HISTORY_FILE = "results/history.json"

# ── HELPERS ───────────────────────────────────────────────────
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    history = history[:10]
    os.makedirs("results", exist_ok=True)
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

# ── MODELS ───────────────────────────────────────────────────
class TextInput(BaseModel):
    text: str

# ── ROUTES ───────────────────────────────────────────────────
@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/analyze")
def analyze(input: TextInput):
    try:
        logger.info(f"Analyzing text of length {len(input.text)}")
        result = analyze_text(input.text)
        entry = {
            "timestamp": datetime.now().strftime("%d %b %Y, %I:%M %p"),
            "text_preview": input.text[:80] + "..." if len(input.text) > 80 else input.text,
            "sentiment": result.get("sentiment", "N/A"),
            "manipulation_level": result.get("manipulation_level", "N/A"),
            "bias": result.get("bias", "N/A"),
            "verdict": result.get("verdict", "N/A")
        }
        save_history(entry)
        return result
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return {"error": str(e)}

@app.get("/history")
def get_history():
    return load_history()

@app.get("/evaluate")
def evaluate():
    try:
        logger.info("Running evaluation...")
        return run_evaluation(analyze_text)
    except Exception as e:
        logger.error(f"Evaluation failed: {e}")
        return {"error": str(e)}

@app.get("/evaluate-real")
def evaluate_real():
    if not REAL_EVAL_AVAILABLE:
        return {"error": "Real evaluator not available. Check imports."}
    try:
        logger.info("Starting real dataset evaluation...")
        return run_real_evaluation(analyze_text, max_samples=200)
    except Exception as e:
        logger.error(f"Real evaluation failed: {e}")
        return {"error": str(e)}