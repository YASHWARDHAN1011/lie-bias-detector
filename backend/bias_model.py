import logging
import os
import sys
from transformers import pipeline

logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("Loading bias model...")
bias_classifier = pipeline(
    "text-classification",
    model="valurank/distilroberta-bias",
    truncation=True,
    max_length=512
)
print("Bias model ready!")
def predict_bias(text):
    """
    Uses trained model as primary signal.
    Keywords only used as tiebreaker when model is uncertain.
    """
    try:
        result = bias_classifier(text)[0]
        label = result["label"].upper()
        score = round(result["score"] * 100, 2)

        # Model is confident — trust it directly
        if score >= 70:
            if "BIASED" in label or "BIAS" in label:
                text_lower = text.lower()
                left_hints = ["progressive", "equality", "climate", "diversity",
                              "welfare", "union", "lgbtq", "feminism", "systemic"]
                right_hints = ["freedom", "patriot", "border", "conservative",
                               "tax cut", "military", "second amendment", "woke",
                               "deep state", "america first"]
                left_score  = sum(1 for w in left_hints  if w in text_lower)
                right_score = sum(1 for w in right_hints if w in text_lower)

                # Subject of criticism matters — attacking "progressive" = right-leaning
                attack_left  = any(p in text_lower for p in
                    ["destroying", "radical", "corrupt", "threat", "agenda",
                     "dangerous", "evil", "shameful"])
                
                if attack_left and left_score > 0:
                    return "Right-leaning", score
                elif left_score > right_score:
                    return "Left-leaning", score
                elif right_score > left_score:
                    return "Right-leaning", score
                else:
                    return "Biased / Unclear", score
            else:
                return "Neutral / Unclear", score

        # Model is uncertain — use keywords as tiebreaker
        else:
            text_lower = text.lower()
            left_hints  = ["progressive", "equality", "climate", "diversity", "welfare"]
            right_hints = ["freedom", "patriot", "border", "conservative", "military"]
            left_score  = sum(1 for w in left_hints  if w in text_lower)
            right_score = sum(1 for w in right_hints if w in text_lower)

            attack_left = any(p in text_lower for p in
                ["destroying", "radical", "dangerous", "agenda", "corrupt"])

            if attack_left and left_score > 0:
                return "Right-leaning", score
            elif left_score > right_score:
                return "Left-leaning", score
            elif right_score > left_score:
                return "Right-leaning", score
            else:
                return "Neutral / Unclear", score

    except Exception as e:
        logger.error(f"Bias model error: {e}")
        return "Neutral / Unclear", 50.0