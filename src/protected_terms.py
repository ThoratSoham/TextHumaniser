"""
src/protected_terms.py — extracts names, places, and organizations from the book
via spaCy NER, so downstream transforms never alter them.

Writes protected_terms.txt at the repo root (one term per line) and exposes
load_protected_terms() for other modules to import.
"""

import spacy
from pathlib import Path
from typing import Set

from src.ingest import stream_paragraphs

PROTECTED_LABELS = {"PERSON", "GPE", "ORG", "NORP"}
DEFAULT_OUTPUT_PATH = "protected_terms.txt"


def extract_protected_terms(filepath: str, nlp=None) -> Set[str]:
    """
    Streams the given book and runs spaCy NER over every paragraph,
    collecting entities of interest into a deduplicated set.
    """
    if nlp is None:
        nlp = spacy.load("en_core_web_sm")

    terms: Set[str] = set()

    for chunk in stream_paragraphs(filepath):
        doc = nlp(chunk["text"])
        for ent in doc.ents:
            if ent.label_ in PROTECTED_LABELS:
                cleaned = ent.text.strip()
                if cleaned:
                    terms.add(cleaned)

    return terms


def save_protected_terms(terms: Set[str], output_path: str = DEFAULT_OUTPUT_PATH) -> None:
    with open(output_path, "w", encoding="utf-8") as f:
        for term in sorted(terms):
            f.write(term + "\n")


def load_protected_terms(path: str = DEFAULT_OUTPUT_PATH) -> Set[str]:
    """
    Loads the protected terms file back into a set. Returns an empty set
    (with a warning printed) if the file doesn't exist yet.
    """
    filepath = Path(path)
    if not filepath.exists():
        print(f"WARNING: {path} not found. Run protected_terms.py as a script first.")
        return set()

    with open(filepath, "r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip()}


if __name__ == "__main__":
    import sys

    input_file = sys.argv[1] if len(sys.argv) > 1 else "data/input/sample_book.txt"
    print(f"Extracting protected terms from: {input_file}")

    terms = extract_protected_terms(input_file)
    save_protected_terms(terms)

    print(f"Found {len(terms)} protected terms. Saved to {DEFAULT_OUTPUT_PATH}")
    print("Review this file and add any missed names/invented terms manually.")
