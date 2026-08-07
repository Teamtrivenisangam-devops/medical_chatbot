import numpy as np
import nltk
from nltk_utils import tokenize, stem, bag_of_words

# Download NLTK data if not already present
nltk.download('punkt', quiet=True)

def test_tokenize():
    sentence = "How are you doing today?"
    tokens = tokenize(sentence)
    assert isinstance(tokens, list)
    assert len(tokens) == 6
    assert "How" in tokens

def test_stem():
    assert stem("organizing") == "organ"
    assert stem("organize") == "organ"
    assert stem("headaches") == "headach"

def test_bag_of_words():
    sentence = ["hello", "how", "are", "you"]
    words = ["hi", "hello", "I", "you", "bye", "thank", "cool"]
    bog = bag_of_words(sentence, words)
    expected = np.array([0., 1., 0., 1., 0., 0., 0.], dtype=np.float32)
    np.testing.assert_array_equal(bog, expected)
