import os
import sys
import logging
from datasets import load_dataset
from sklearn.metrics import (
    accuracy_score, precision_score,
    recall_score, f1_score, confusion_matrix
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyzer import analyze_text

logger = logging.getLogger(__name__)

# ── SST-2 SENTIMENT EVALUATION ────────────────────────────────
def evaluate_sentiment_sst2(analyzer_func, max_samples=200):
    """
    Evaluates sentiment on real SST-2 dataset
    SST-2 labels: 0 = negative, 1 = positive
    We use 200 samples for speed — full set is 872
    """
    logger.info("Loading SST-2 dataset...")
    dataset = load_dataset("glue", "sst2", split="validation")
    dataset = dataset.select(range(min(max_samples, len(dataset))))

    true_labels = []
    pred_labels = []
    errors = []

    for i, sample in enumerate(dataset):
        text = sample["sentence"]
        true = "Positive" if sample["label"] == 1 else "Negative"

        result = analyzer_func(text)
        pred = result.get("sentiment", "Neutral")

        # SST-2 is binary — map Neutral predictions to closest
        if pred == "Neutral":
            conf = float(result.get("confidence", "50%").replace("%", ""))
            pred = "Positive" if conf >= 50 else "Negative"

        true_labels.append(true)
        pred_labels.append(pred)

        if pred != true:
            errors.append({
                "text": text[:100],
                "true": true,
                "predicted": pred,
                "confidence": result.get("confidence", "N/A")
            })

        if i % 50 == 0:
            logger.info(f"SST-2 progress: {i}/{max_samples}")

    labels = ["Positive", "Negative"]
    accuracy  = round(accuracy_score(true_labels, pred_labels) * 100, 1)
    precision = round(precision_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    recall    = round(recall_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    f1        = round(f1_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    cm        = confusion_matrix(true_labels, pred_labels, labels=labels).tolist()

    return {
        "dataset": "SST-2 (Stanford Sentiment Treebank)",
        "samples": max_samples,
        "accuracy":  accuracy,
        "precision": precision,
        "recall":    recall,
        "f1":        f1,
        "confusion_matrix": cm,
        "labels": labels,
        "errors": errors[:10],
        "error_count": len(errors)
    }


# ── LIAR DATASET MANIPULATION EVALUATION ─────────────────────
def evaluate_manipulation_liar(analyzer_func, max_samples=200):
    """
    Evaluates manipulation detection on LIAR dataset
    LIAR labels: pants-fire, false, barely-true → fake/manipulative
                 half-true, mostly-true, true    → real/credible
    We map these to High/Medium/Low manipulation
    """
    logger.info("Loading LIAR dataset...")
    dataset = load_dataset("liar", split="test", trust_remote_code=True)
    dataset = dataset.select(range(min(max_samples, len(dataset))))

    true_labels = []
    pred_labels = []
    errors = []

    # Map LIAR labels to manipulation levels
    liar_to_manip = {
        "pants-fire": "High",
        "false":      "High",
        "barely-true":"Medium",
        "half-true":  "Medium",
        "mostly-true":"Low",
        "true":       "Low"
    }

    for i, sample in enumerate(dataset):
        text = sample["statement"]
        liar_label = sample["label"]

        # Some versions use integers
        int_to_str = {
            0: "pants-fire",
            1: "false",
            2: "barely-true",
            3: "half-true",
            4: "mostly-true",
            5: "true"
        }
        if isinstance(liar_label, int):
            liar_label = int_to_str.get(liar_label, "half-true")

        true = liar_to_manip.get(liar_label, "Medium")
        result = analyzer_func(text)
        pred = result.get("manipulation_level", "Low")

        true_labels.append(true)
        pred_labels.append(pred)

        if pred != true:
            errors.append({
                "text": text[:100],
                "true": true,
                "predicted": pred,
                "liar_label": liar_label
            })

        if i % 50 == 0:
            logger.info(f"LIAR progress: {i}/{max_samples}")

    labels = ["High", "Medium", "Low"]
    accuracy  = round(accuracy_score(true_labels, pred_labels) * 100, 1)
    precision = round(precision_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    recall    = round(recall_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    f1        = round(f1_score(true_labels, pred_labels, average="weighted", zero_division=0) * 100, 1)
    cm        = confusion_matrix(true_labels, pred_labels, labels=labels).tolist()

    return {
        "dataset": "LIAR (Political Statements Fact-Check Dataset)",
        "samples": max_samples,
        "accuracy":  accuracy,
        "precision": precision,
        "recall":    recall,
        "f1":        f1,
        "confusion_matrix": cm,
        "labels": labels,
        "errors": errors[:10],
        "error_count": len(errors)
    }


# ── COMBINED EVALUATION ───────────────────────────────────────
def run_real_evaluation(analyzer_func, max_samples=200):
    """
    Runs evaluation on both real public datasets
    """
    logger.info("Starting real dataset evaluation...")

    results = {}

    try:
        results["sentiment"] = evaluate_sentiment_sst2(analyzer_func, max_samples)
        logger.info(f"SST-2 accuracy: {results['sentiment']['accuracy']}%")
    except Exception as e:
        logger.error(f"SST-2 evaluation failed: {e}")
        results["sentiment"] = {"error": str(e)}

    try:
        results["manipulation"] = evaluate_manipulation_liar(analyzer_func, max_samples)
        logger.info(f"LIAR accuracy: {results['manipulation']['accuracy']}%")
    except Exception as e:
        logger.error(f"LIAR evaluation failed: {e}")
        results["manipulation"] = {"error": str(e)}

    results["note"] = (
        "Evaluated on real public datasets. "
        "SST-2 is a binary sentiment benchmark. "
        "LIAR is a political fact-check dataset mapped to manipulation levels."
    )

    return results