"""
src/scoring.py — pure-Python "naturalness" scorer, no ML model required.

Combines sentence-length variance (burstiness), average word length,
function-word ratio, and phrase-bank hit count into a single 0-1 score.
Higher = more human-like by these statistical proxies.
"""

import re
import statistics
import spacy

from src.transforms.phrase_bank import PHRASE_BANK, _PATTERN as PHRASE_PATTERN

# --- tunable weights, documented here for easy adjustment ---
WEIGHT_BURSTINESS = 0.35       # sentence-length stdev — higher variance = more human
WEIGHT_WORD_LENGTH_VARIANCE = 0.15  # word-length stdev — humans vary word choice length too
WEIGHT_FUNCTION_WORD_RATIO = 0.20   # deviation from a "natural" function-word ratio
WEIGHT_PHRASE_PENALTY = 0.30        # penalty for remaining AI-typical transition phrases

_TARGET_FUNCTION_WORD_RATIO = 0.45  # rough natural-English baseline
_MAX_EXPECTED_STDEV = 10.0          # normalization ceiling for sentence-length stdev


def _sentence_lengths(doc) -> list:
    return [sum(1 for t in sent if not t.is_punct) for sent in doc.sents]


def _word_lengths(doc) -> list:
    return [len(t.text) for t in doc if t.is_alpha]


def _function_word_ratio(doc) -> float:
    content_tokens = [t for t in doc if t.is_alpha]
    if not content_tokens:
        return 0.0
    function_count = sum(1 for t in content_tokens if t.is_stop)
    return function_count / len(content_tokens)


def _phrase_bank_hits(text: str) -> int:
    return len(PHRASE_PATTERN.findall(text))


def humanness_score(text: str, nlp=None) -> float:
    """
    Returns a float 0-1 estimating how "human-natural" the text reads,
    based on sentence-length variance, word-length variance, function-word
    ratio, and remaining AI-typical phrase count. No ML model required.
    """
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)

    sent_lengths = _sentence_lengths(doc)
    burstiness = statistics.stdev(sent_lengths) if len(sent_lengths) > 1 else 0.0
    burstiness_score = min(burstiness / _MAX_EXPECTED_STDEV, 1.0)

    word_lengths = _word_lengths(doc)
    word_len_stdev = statistics.stdev(word_lengths) if len(word_lengths) > 1 else 0.0
    word_len_score = min(word_len_stdev / 3.0, 1.0)  # ~3.0 stdev is a natural ceiling for English

    fw_ratio = _function_word_ratio(doc)
    fw_score = 1.0 - min(abs(fw_ratio - _TARGET_FUNCTION_WORD_RATIO) / _TARGET_FUNCTION_WORD_RATIO, 1.0)

    phrase_hits = _phrase_bank_hits(text)
    phrase_score = max(1.0 - (phrase_hits * 0.25), 0.0)  # each hit costs 0.25, floors at 0

    score = (
        WEIGHT_BURSTINESS * burstiness_score
        + WEIGHT_WORD_LENGTH_VARIANCE * word_len_score
        + WEIGHT_FUNCTION_WORD_RATIO * fw_score
        + WEIGHT_PHRASE_PENALTY * phrase_score
    )

    return round(min(max(score, 0.0), 1.0), 3)


if __name__ == "__main__":
    from src.transforms.synonym_sub import substitute_synonyms
    from src.transforms.sentence_reshape import reshape_sentences
    from src.transforms.phrase_bank import substitute_phrases
    from src.transforms.noise import inject_noise

    with open("test_paragraph.txt", "r", encoding="utf-8") as f:
        sample = f.read().strip()

    before_score = humanness_score(sample)

    transformed = substitute_phrases(sample)
    transformed = reshape_sentences(transformed, split_probability=0.6, merge_probability=0.3)
    transformed = substitute_synonyms(transformed, protected_terms={"Maria"}, swap_probability=0.2)
    transformed = inject_noise(transformed, intensity=0.4)

    after_score = humanness_score(transformed)

    print(f"BEFORE score: {before_score}")
    print(f"Text: {sample}\n")
    print(f"AFTER score: {after_score}")
    print(f"Text: {transformed}")
