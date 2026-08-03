"""
src/transforms/phrase_bank.py — swaps common AI-typical transition phrases
for varied, more casual human alternatives.
"""

import re
import random

PHRASE_BANK = {
    "furthermore": ["also", "plus", "on top of that", "and"],
    "moreover": ["also", "what's more", "on top of that", "and"],
    "however": ["but", "still", "even so", "that said"],
    "in conclusion": ["so in the end", "all told", "in the end", "ultimately"],
    "it is important to note that": ["worth noting,", "it's worth mentioning that", "notably,"],
    "it is important to note": ["worth noting", "it's worth mentioning", "notably"],
    "delve into": ["dig into", "look closely at", "explore"],
    "in today's world": ["these days", "nowadays", "in this day and age"],
    "on the other hand": ["then again", "but then", "conversely"],
    "as a result": ["so", "because of that", "which meant"],
    "in order to": ["to"],
    "due to the fact that": ["because", "since"],
    "a variety of": ["several", "a range of", "many kinds of"],
    "it goes without saying": ["obviously", "clearly", "needless to say"],
    "at the end of the day": ["ultimately", "in the end", "when it came down to it"],
}

# build a single regex matching any phrase-bank key, longest-first to avoid partial overlaps
_SORTED_KEYS = sorted(PHRASE_BANK.keys(), key=len, reverse=True)
_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(k) for k in _SORTED_KEYS) + r")\b",
    re.IGNORECASE,
)


def substitute_phrases(text: str) -> str:
    """
    Finds AI-typical transition phrases (case-insensitive) in `text` and
    replaces each occurrence with a randomly chosen casual alternative.
    """

    def _replace(match: re.Match) -> str:
        matched_text = match.group(0)
        key = matched_text.lower()
        alternatives = PHRASE_BANK.get(key)
        if not alternatives:
            return matched_text
        replacement = random.choice(alternatives)
        # preserve capitalization if the matched phrase started a sentence
        if matched_text[0].isupper():
            replacement = replacement[0].upper() + replacement[1:]
        return replacement

    return _PATTERN.sub(_replace, text)


if __name__ == "__main__":
    with open("test_paragraph.txt", "r", encoding="utf-8") as f:
        sample = f.read().strip()

    print("BEFORE:\n" + sample)
    random.seed(3)
    print("\nAFTER:\n" + substitute_phrases(sample))
