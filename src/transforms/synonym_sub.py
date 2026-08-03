"""
src/transforms/synonym_sub.py — WordNet-based synonym substitution.

Replaces eligible content words with contextually-plausible synonyms,
skipping protected terms (names/places) and function words (stopwords).
"""

import random
import spacy
from nltk.corpus import wordnet

# spaCy POS tag -> WordNet POS tag mapping
_POS_MAP = {
    "NOUN": wordnet.NOUN,
    "VERB": wordnet.VERB,
    "ADJ": wordnet.ADJ,
    "ADV": wordnet.ADV,
}

# words we never want to touch even if grammatically eligible
_SKIP_POS = {"PROPN", "PRON", "DET", "ADP", "CCONJ", "SCONJ", "PART", "AUX", "NUM", "PUNCT", "SYM", "SPACE"}


def _get_synonyms(word: str, wn_pos: str) -> list:
    synonyms = set()
    for syn in wordnet.synsets(word, pos=wn_pos):
        for lemma in syn.lemmas():
            candidate = lemma.name().replace("_", " ")
            if candidate.lower() != word.lower() and candidate.isalpha():
                synonyms.add(candidate)
    return list(synonyms)


def substitute_synonyms(text: str, protected_terms: set, swap_probability: float = 0.15, nlp=None) -> str:
    """
    Replaces eligible content words in `text` with a WordNet synonym,
    chosen probabilistically per-word based on swap_probability.
    Skips protected_terms, stopwords, and non-content POS categories.
    """
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    doc = nlp(text)
    result_tokens = []

    for token in doc:
        word = token.text

        should_consider = (
            not token.is_stop
            and not token.is_punct
            and token.pos_ not in _SKIP_POS
            and word not in protected_terms
            and word.lower() not in {t.lower() for t in protected_terms}
            and token.pos_ in _POS_MAP
        )

        if should_consider and random.random() < swap_probability:
            wn_pos = _POS_MAP[token.pos_]
            synonyms = _get_synonyms(word.lower(), wn_pos)
            if synonyms:
                chosen = random.choice(synonyms)
                # preserve capitalization if original word was capitalized
                if word[0].isupper():
                    chosen = chosen[0].upper() + chosen[1:]
                result_tokens.append(chosen + token.whitespace_)
                continue

        result_tokens.append(word + token.whitespace_)

    return "".join(result_tokens)


if __name__ == "__main__":
    with open("test_paragraph.txt", "r", encoding="utf-8") as f:
        sample = f.read().strip()

    protected = {"Maria"}
    print("BEFORE:\n" + sample)
    print("\nAFTER:\n" + substitute_synonyms(sample, protected, swap_probability=0.25))
