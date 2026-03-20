try:
    from bias_model import predict_bias
    BIAS_MODEL_AVAILABLE = True
    print("Trained bias model loaded!")
except Exception as e:
    BIAS_MODEL_AVAILABLE = False
    print(f"Bias model not available, using keywords: {e}")
from transformers import pipeline
from backend.words import (
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
    # Primary model — SST-2 (positive/negative)
    result = sentiment_model(text, truncation=True, max_length=512)[0]
    label = result["label"]
    score = round(result["score"] * 100, 2)

    # Proper 3-class logic based on linguistic signals
    text_lower = text.lower()
    
    # Neutral indicators — factual reporting language
    neutral_signals = [
        "according to", "officials say", "reports suggest",
        "study finds", "data shows", "analysts say",
        "announced", "confirmed", "stated", "said"
    ]
    
    has_neutral_signal = any(sig in text_lower for sig in neutral_signals)
    
    # If text has neutral reporting language AND model isn't very confident
    if has_neutral_signal and score < 85:
        sentiment = "Neutral"
    elif score < 60:
        # Genuinely uncertain — call it neutral
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
    found_left  = [w for w in left_words  if w in text_lower]
    found_right = [w for w in right_words if w in text_lower]

    if BIAS_MODEL_AVAILABLE:
        try:
            model_bias, confidence = predict_bias(text)
            keyword_left  = len(found_left)
            keyword_right = len(found_right)
            if model_bias == "Neutral / Unclear" and keyword_left > keyword_right:
                bias = "Left-leaning"
            elif model_bias == "Neutral / Unclear" and keyword_right > keyword_left:
                bias = "Right-leaning"
            else:
                bias = model_bias
        except Exception as e:
            print(f"Bias prediction error: {e}")
            bias = "Neutral / Unclear"
    else:
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

def explain_prediction(text, trigger_words, bias_words_found, sentiment):
    text_lower = text.lower()
    words = text.split()
    explained = []

    for word in words:
        word_clean = word.lower().strip('.,!?";:')
        if any(tw in word_clean for tw in trigger_words if tw != "None found"):
            explained.append({"word": word, "type": "manipulation"})
        elif any(bw in word_clean for bw in bias_words_found if bw != "None found"):
            explained.append({"word": word, "type": "bias"})
        else:
            explained.append({"word": word, "type": "normal"})

    # Build explanation sentences
    reasons = []
    if trigger_words and trigger_words != ["None found"]:
        reasons.append(f"Manipulation detected because of: {', '.join(trigger_words[:5])}")
    if bias_words_found and bias_words_found != ["None found"]:
        reasons.append(f"Bias indicators found: {', '.join(bias_words_found[:5])}")
    if sentiment == "Negative":
        reasons.append("Sentiment model detected strong negative tone")
    elif sentiment == "Positive":
        reasons.append("Sentiment model detected positive tone")

    return {
        "word_breakdown": explained,
        "reasons": reasons
    }

def analyze_text(text):
    if not text or len(text.strip()) == 0:
        return {"error": "Please enter some text to analyze."}

    sentiment, confidence        = analyze_sentiment(text)
    manipulation, trigger_words  = analyze_manipulation(text)
    bias, left_found, right_found = analyze_bias(text)
    verdict                      = generate_verdict(sentiment, manipulation, bias)
    bias_words_found             = left_found + right_found

    explanation = explain_prediction(
        text, 
        trigger_words if trigger_words else [], 
        bias_words_found if bias_words_found else [],
        sentiment
    )

    return {
        "sentiment":          sentiment,
        "confidence":         f"{confidence}%",
        "manipulation_level": manipulation,
        "bias":               bias,
        "trigger_words":      trigger_words      if trigger_words      else ["None found"],
        "bias_words_found":   bias_words_found   if bias_words_found   else ["None found"],
        "verdict":            verdict,
        "word_breakdown":     explanation["word_breakdown"],
        "reasons":            explanation["reasons"]
    }