"""
src/transforms/sentence_reshape.py — restructures sentence length distribution.

Splits long sentences at conjunction points and merges short adjacent sentences,
both applied probabilistically to avoid a mechanical, uniform pattern.
"""

import random
import spacy

_SPLIT_CONJUNCTIONS = {"and", "but", "so", "because", "while", "although"}
_MERGE_CONNECTORS = ["and", "and then", "while", "as"]
_SHORT_SENTENCE_WORD_THRESHOLD = 8
_LONG_SENTENCE_WORD_THRESHOLD = 20


def _find_split_point(sent) -> int:
    """Finds a token index to split at, preferring a coordinating conjunction
    roughly in the middle of the sentence. Returns -1 if none found."""
    tokens = list(sent)
    mid = len(tokens) // 2
    best_idx = -1
    best_distance = float("inf")

    for i, token in enumerate(tokens):
        if token.text.lower() in _SPLIT_CONJUNCTIONS and token.pos_ in {"CCONJ", "SCONJ"}:
            distance = abs(i - mid)
            if distance < best_distance:
                best_distance = distance
                best_idx = i

    return best_idx


def _split_sentence(sent) -> list:
    tokens = list(sent)
    split_idx = _find_split_point(sent)

    if split_idx <= 0 or split_idx >= len(tokens) - 1:
        return [sent.text]

    first_half = "".join(t.text_with_ws for t in tokens[:split_idx]).strip()
    second_half = "".join(t.text_with_ws for t in tokens[split_idx + 1:]).strip()

    if not first_half or not second_half:
        return [sent.text]

    # capitalize the start of the new second sentence
    second_half = second_half[0].upper() + second_half[1:]
    if not first_half.endswith((".", "!", "?")):
        first_half += "."

    return [first_half, second_half]


def reshape_sentences(text: str, split_probability: float = 0.2, merge_probability: float = 0.1, nlp=None) -> str:
    """
    Restructures sentence boundaries in `text`: probabilistically splits long
    sentences at conjunction points, and probabilistically merges short
    adjacent sentences with a connector. Returns the reshaped text.
    """
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    sentences = list(doc.sents)

    # Pass 1: splitting
    expanded = []
    for sent in sentences:
        word_count = sum(1 for t in sent if not t.is_punct)
        if word_count >= _LONG_SENTENCE_WORD_THRESHOLD and random.random() < split_probability:
            expanded.extend(_split_sentence(sent))
        else:
            expanded.append(sent.text.strip())

    # Pass 2: merging short adjacent sentences
    merged = []
    skip_next = False
    for i, sent_text in enumerate(expanded):
        if skip_next:
            skip_next = False
            continue

        word_count = len(sent_text.split())
        if (
            word_count <= _SHORT_SENTENCE_WORD_THRESHOLD
            and i + 1 < len(expanded)
            and random.random() < merge_probability
        ):
            connector = random.choice(_MERGE_CONNECTORS)
            next_sent = expanded[i + 1]
            # lowercase the start of the sentence being merged in
            next_sent_lower = next_sent[0].lower() + next_sent[1:] if next_sent else next_sent
            combined = sent_text.rstrip(".!?") + f", {connector} " + next_sent_lower
            merged.append(combined)
            skip_next = True
        else:
            merged.append(sent_text)

    return " ".join(merged)


if __name__ == "__main__":
    with open("test_paragraph.txt", "r", encoding="utf-8") as f:
        sample = f.read().strip()

    print("BEFORE:\n" + sample)
    random.seed(7)
    print("\nAFTER:\n" + reshape_sentences(sample, split_probability=0.8, merge_probability=0.5))
