import sys
import os

# Add both root and backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from analyzer import analyze_text

def test_negative_sentiment():
    result = analyze_text("This is absolutely terrible and disgusting.")
    assert result["sentiment"] == "Negative"
    print("✅ test_negative_sentiment passed")

def test_positive_sentiment():
    result = analyze_text("This is wonderful and amazing!")
    assert result["sentiment"] == "Positive"
    print("✅ test_positive_sentiment passed")

def test_high_manipulation():
    result = analyze_text("The radical corrupt regime is destroying everything and nobody sees it!")
    assert result["manipulation_level"] == "High"
    print("✅ test_high_manipulation passed")

def test_low_manipulation():
    result = analyze_text("According to officials, the committee announced a new agreement.")
    assert result["manipulation_level"] == "Low"
    print("✅ test_low_manipulation passed")

def test_output_keys():
    result = analyze_text("Some random text here.")
    required_keys = ["sentiment", "confidence", "manipulation_level", "bias", 
                     "trigger_words", "bias_words_found", "verdict"]
    for key in required_keys:
        assert key in result, f"Missing key: {key}"
    print("✅ test_output_keys passed")

def test_empty_input():
    result = analyze_text("")
    assert "error" in result
    print("✅ test_empty_input passed")

if __name__ == "__main__":
    print("\nRunning unit tests...\n")
    test_output_keys()
    test_empty_input()
    test_negative_sentiment()
    test_positive_sentiment()
    test_high_manipulation()
    test_low_manipulation()
    print("\n✅ All tests passed!\n")