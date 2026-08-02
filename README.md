# TextHumaniser

An offline, rule-based NLP pipeline that transforms long-form text — rewriting sentence structure, lexical choices, and phrasing — while preserving the original meaning, characters, and story. Built entirely with classical NLP techniques (spaCy, WordNet), not generative AI, so it runs fully local with no API costs, no rate limits, and no internet dependency once set up.

## Why

Most text-generation output (AI or otherwise) tends toward uniform sentence length, repetitive transition phrases, and predictable word choices. This project applies a set of measurable, tunable transformations — synonym substitution, sentence splitting/merging, phrase-bank replacement, controlled noise — to shift those statistical patterns while keeping a scoring system in the loop to check the result still reads naturally.

Originally built to process a full book-length manuscript on modest hardware (16GB RAM, no GPU), so streaming/checkpointed processing for large documents was a design requirement from the start, not an afterthought.

## How it works

1. **Ingest** — streams the input document (`.txt` or `.docx`) paragraph by paragraph rather than loading it fully into memory, so book-length input is handled the same way as a single paragraph.
2. **Protect** — extracts names, places, and proper nouns via spaCy NER so they're never altered by downstream transforms.
3. **Transform** — applies four independent, tunable passes:
   - Synonym substitution (WordNet, POS-aware)
   - Sentence splitting/merging (spaCy dependency parsing)
   - Phrase-bank substitution (swaps generic/robotic transition phrases for varied alternatives)
   - Controlled noise injection (light punctuation/contraction variation)
4. **Score** — a pure-Python "naturalness" score (sentence-length variance, word-length distribution, phrase repetition) checks each paragraph after transformation; low-scoring paragraphs get a second pass with adjusted intensity.
5. **Checkpoint** — every processed paragraph is written to disk immediately, so processing a large document can be safely interrupted and resumed without reprocessing earlier work.
6. **Reassemble** — stitches the processed paragraphs back into a single output document matching the original structure (chapters, headings).

## Project status

Built in phases — see `PROJECT_GUIDE.md` for the full build plan, including the exact spec/prompt used to generate each module. Track progress via the repo's Issues/Projects tab.

- [ ] Phase 0 — Environment setup
- [ ] Phase 1 — Streaming ingestion
- [ ] Phase 2 — Protected terms extraction
- [ ] Phase 3 — Transform functions (synonym sub, sentence reshape, phrase bank, noise)
- [ ] Phase 4 — Naturalness scoring
- [ ] Phase 5 — Pipeline + checkpointing
- [ ] Phase 6 — Reassembly
- [ ] Phase 7 — Manual QA pass

## Requirements

- Python 3.10+
- No GPU required — all components run on CPU
- See `requirements.txt` for dependencies (spaCy, NLTK, gensim, python-docx, tqdm)

## Setup

```bash
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"
```

## Usage

```bash
python src/pipeline.py --input data/input/your_document.docx --output data/output/
```

Progress is checkpointed to `checkpoints/` — if interrupted, re-running the same command resumes from the last completed paragraph instead of starting over.

## Project structure

```
├── src/
│   ├── ingest.py
│   ├── protected_terms.py
│   ├── transforms/
│   ├── scoring.py
│   ├── pipeline.py
│   └── reassemble.py
├── protected_terms.txt
├── test_paragraph.txt
├── checkpoints/         (gitignored)
├── data/                (gitignored)
└── PROJECT_GUIDE.md
```

## Notes

- Input documents are gitignored — this repo tracks code, not content.
- Tuning parameters (swap probability, split probability, noise intensity) are exposed as function arguments in each transform module — see `PROJECT_GUIDE.md` for defaults and tuning guidance.
- This is a text-transformation tool, not a content-generation tool: no new sentences or facts are introduced, only restructuring and substitution of existing text.

ll
