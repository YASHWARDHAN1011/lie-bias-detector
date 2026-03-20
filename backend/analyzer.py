from transformers import pipeline
from words import (
    fear_words, loaded_words, exaggeration_words, clickbait_words,
    ALL_MANIPULATION_WORDS, left_words, right_words, neutral_words
)

# ============================================================
# LOAD MODEL
# ============================================================

print("Loading sentiment model...")
sentiment_model = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)
print("Model ready!")


# ============================================================
# SENTIMENT ANALYSIS
# ============================================================

def analyze_sentiment(text):
    result = sentiment_model(text, truncation=True, max_length=512)[0]
    label = result["label"]
    score = round(result["score"] * 100, 2)

    if score < 65:
        sentiment = "Neutral"
    elif label == "POSITIVE":
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    return sentiment, score


# ============================================================
# MANIPULATION DETECTION
# ============================================================

def analyze_manipulation(text):
    text_lower = text.lower()
    words_in_text = text_lower.split()

    found_fear         = [w for w in fear_words         if w in text_lower]
    found_loaded       = [w for w in loaded_words       if w in text_lower]
    found_exaggeration = [w for w in exaggeration_words if w in words_in_text]
    found_clickbait    = [w for w in clickbait_words    if w in text_lower]

    all_found = found_fear + found_loaded + found_exaggeration + found_clickbait
    total = len(all_found)

    if total == 0:
        level = "Low"
    elif total <= 2:
        level = "Medium"
    else:
        level = "High"

    return level, all_found


# ============================================================
# BIAS DETECTION
# ============================================================

def analyze_bias(text):
    text_lower = text.lower()

    found_left    = [w for w in left_words    if w in text_lower]
    found_right   = [w for w in right_words   if w in text_lower]
    found_neutral = [w for w in neutral_words if w in text_lower]

    left_score  = len(found_left)
    right_score = len(found_right)

    if left_score == 0 and right_score == 0:
        bias = "Neutral / Unclear"
    elif left_score > right_score:
        bias = "Left-leaning"
    elif right_score > left_score:
        bias = "Right-leaning"
    else:
        bias = "Mixed / Unclear"

    return bias, found_left, found_right


# ============================================================
# VERDICT GENERATOR
# ============================================================

def generate_verdict(sentiment, manipulation_level, bias):
    parts = []

    if sentiment == "Negative":
        parts.append("This text has a strongly negative tone.")
    elif sentiment == "Positive":
        parts.append("This text has a positive tone.")
    else:
        parts.append("This text has a relatively neutral tone.")

    if manipulation_level == "High":
        parts.append("It contains a high amount of emotionally loaded and manipulative language.")
    elif manipulation_level == "Medium":
        parts.append("Some emotionally charged words were detected.")
    else:
        parts.append("No significant manipulation language was found.")

    if bias == "Left-leaning":
        parts.append("The language appears to lean left based on detected keywords.")
    elif bias == "Right-leaning":
        parts.append("The language appears to lean right based on detected keywords.")
    elif bias == "Mixed / Unclear":
        parts.append("Mixed bias signals were detected.")
    else:
        parts.append("No strong political bias was detected.")

    return " ".join(parts)


# ============================================================
# MAIN FUNCTION
# ============================================================

def analyze_text(text):
    if not text or len(text.strip()) == 0:
        return {"error": "Please enter some text to analyze."}

    sentiment, confidence        = analyze_sentiment(text)
    manipulation, trigger_words  = analyze_manipulation(text)
    bias, left_found, right_found = analyze_bias(text)
    verdict                      = generate_verdict(sentiment, manipulation, bias)
    bias_words_found             = left_found + right_found

    return {
        "sentiment":          sentiment,
        "confidence":         f"{confidence}%",
        "manipulation_level": manipulation,
        "bias":               bias,
        "trigger_words":      trigger_words      if trigger_words      else ["None found"],
        "bias_words_found":   bias_words_found   if bias_words_found   else ["None found"],
        "verdict":            verdict
    }