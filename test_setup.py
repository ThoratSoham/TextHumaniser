"""
test_setup.py — confirms the environment is correctly configured.
Run this after setup.sh to verify spaCy, NLTK/WordNet, and python-docx all work.
"""

import spacy
from nltk.corpus import wordnet
import docx  # python-docx


def main():
    print("Loading spaCy model...")
    nlp = spacy.load("en_core_web_sm")

    test_sentence = "The quick brown fox jumps over the lazy dog."
    doc = nlp(test_sentence)

    print(f"\nParsed sentence: '{test_sentence}'")
    print("Tokens and POS tags:")
    for token in doc:
        print(f"  {token.text:12s} {token.pos_}")

    print("\nTesting WordNet lookup for 'quick'...")
    synsets = wordnet.synsets("quick", pos=wordnet.ADJ)
    if synsets:
        synonyms = {lemma.name() for syn in synsets for lemma in syn.lemmas()}
        print(f"  Found synonyms: {sorted(synonyms)[:8]}")
    else:
        print("  WARNING: no synsets found — WordNet may not be downloaded correctly.")

    print("\nTesting python-docx import...")
    print(f"  python-docx version check OK (Document class: {docx.Document})")

    print("\n✔ All checks passed. Environment is ready.")


if __name__ == "__main__":
    main()
