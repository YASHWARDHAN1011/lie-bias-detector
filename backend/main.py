from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from analyzer import analyze_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

HISTORY_FILE = "results/history.json"

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_history(entry):
    history = load_history()
    history.insert(0, entry)
    history = history[:10]  # keep last 10 only
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

class TextInput(BaseModel):
    text: str

@app.get("/")
def serve_frontend():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
def analyze(input: TextInput):
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

@app.get("/history")
def get_history():
    return load_history()