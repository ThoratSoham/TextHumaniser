"""
src/transforms/noise.py — light, controlled human-like variation.

Contracts formal phrasing, occasionally swaps a comma for an em-dash,
applied probabilistically. Never breaks grammar.
"""

import re
import random

_CONTRACTIONS = {
    r"\bit is\b": "it's",
    r"\bIt is\b": "It's",
    r"\bthat is\b": "that's",
    r"\bThat is\b": "That's",
    r"\bdo not\b": "don't",
    r"\bDo not\b": "Don't",
    r"\bdoes not\b": "doesn't",
    r"\bDoes not\b": "Doesn't",
    r"\bwas not\b": "wasn't",
    r"\bWas not\b": "Wasn't",
    r"\bhad not\b": "hadn't",
    r"\bHad not\b": "Hadn't",
    r"\bwould not\b": "wouldn't",
    r"\bWould not\b": "Wouldn't",
    r"\bcould not\b": "couldn't",
    r"\bCould not\b": "Couldn't",
    r"\bshe would\b": "she'd",
    r"\bhe would\b": "he'd",
    r"\bthey would\b": "they'd",
}


def inject_noise(text: str, intensity: float = 0.1) -> str:
    """
    Adds light human-like variation to `text`: probabilistic contraction of
    formal phrases and occasional comma-to-em-dash swaps. `intensity` scales
    how often each eligible spot is actually changed (0.0 = no changes).
    """
    result = text

    # contraction pass — each match is only contracted with probability = intensity
    for pattern, contraction in _CONTRACTIONS.items():
        def _maybe_contract(match, contraction=contraction):
            return contraction if random.random() < intensity else match.group(0)

        result = re.sub(pattern, _maybe_contract, result)

    # occasional comma -> em-dash swap (only mid-sentence commas, not in lists)
    def _maybe_dash(match):
        return " — " if random.random() < (intensity * 0.5) else match.group(0)

    result = re.sub(r", ", _maybe_dash, result)

    return result


if __name__ == "__main__":
    with open("test_paragraph.txt", "r", encoding="utf-8") as f:
        sample = f.read().strip()

    print("BEFORE:\n" + sample)
    random.seed(5)
    print("\nAFTER:\n" + inject_noise(sample, intensity=0.5))
