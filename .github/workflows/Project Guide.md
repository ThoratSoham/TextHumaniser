# Book Humanizer — Project Guide

Offline, free, pure-NLP pipeline that transforms AI-generated text (paragraph or full book) to reduce AI-detector signals while preserving story, theme, and meaning. No paid APIs, no GPU required.

**How to use this file:** Work top to bottom, one phase at a time. Each phase has a "Prompt to use" block — copy that into your coding assistant *as-is* for that phase only. Don't skip ahead. Check off the box when a phase is tested and working before moving to the next.

---

## 0. Repo structure (target state)

```
your-repository/
├── PROJECT_GUIDE.md          <- this file
├── requirements.txt
├── data/
│   ├── input/                 <- source book files go here (gitignored)
│   └── output/                <- processed results (gitignored)
├── checkpoints/                <- per-paragraph progress + resume state (gitignored)
├── protected_terms.txt         <- names/places never to swap (Phase 2 output, hand-editable)
├── test_paragraph.txt          <- 3-4 real sample paragraphs, used to eyeball every change
├── src/
│   ├── ingest.py               <- Phase 1: streaming file reader + chunker
│   ├── protected_terms.py      <- Phase 2: NER-based protected word extraction
│   ├── transforms/
│   │   ├── synonym_sub.py      <- Phase 3.1
│   │   ├── sentence_reshape.py <- Phase 3.2
│   │   ├── phrase_bank.py      <- Phase 3.3
│   │   └── noise.py            <- Phase 3.4
│   ├── scoring.py               <- Phase 4: humanness scorer
│   ├── pipeline.py              <- Phase 5: wires it all together + checkpointing
│   └── reassemble.py            <- Phase 6: stitches output back into a document
├── .gitignore                   <- must exclude data/, checkpoints/, *.docx, *.txt book files
└── README.md                    <- short public-facing description (separate from this file)
```

Add to `.gitignore` immediately: your actual book text is personal content and checkpoints will be large — don't commit either.

---

## Phase 0 — Environment Setup
**Status:** ☐ not started

**Goal:** working Python env, all libraries importable, spaCy model loads.

**Prompt to use:**
> "Set up a Python virtual environment for this project. Create a `requirements.txt` with: spacy, nltk, gensim, python-docx, tqdm. Write a `setup.sh` (or setup.py step) that installs requirements, downloads the spaCy `en_core_web_sm` model, and downloads the NLTK `wordnet` and `omw-1.4` corpora. Then write a tiny `test_setup.py` that imports everything and parses one test sentence with spaCy to confirm it works."

**Done when:** `python test_setup.py` runs with no errors and prints a parsed sentence.

---

## Phase 1 — Ingestion (streaming, handles big books)
**Status:** ☐ not started

**Goal:** never load the full book into memory; read paragraph-by-paragraph with chapter/paragraph indices attached.

**Prompt to use:**
> "Write `src/ingest.py`. It should expose a generator function `stream_paragraphs(filepath)` that reads either a `.txt` or `.docx` file and yields one paragraph at a time (never the whole file into memory), each yielded as a dict: `{chapter, para_index, text}`. For `.txt`, split on double newlines and detect chapter breaks with a configurable regex (default: lines starting with 'Chapter'). For `.docx`, iterate paragraph objects with python-docx and use heading styles to detect chapter breaks. Include a `test_ingest.py` that runs this on a small sample file and prints the first 5 chunks."

**Done when:** it correctly streams a real sample chapter without loading the whole book into a list.

---

## Phase 2 — Protected Terms Extraction
**Status:** ☐ not started

**Goal:** a list of names/places/invented terms that must never be synonym-swapped.

**Prompt to use:**
> "Write `src/protected_terms.py`. It should read the full book (using `stream_paragraphs` from Phase 1), run spaCy NER over each paragraph, and collect all entities labeled PERSON, GPE, ORG, and NORP into a deduplicated set. Write the result, one term per line, to `protected_terms.txt` at the repo root. Also expose a function `load_protected_terms()` that other modules can import to get this set back as a Python set."

**Done when:** `protected_terms.txt` is generated from your real book and you've manually reviewed/edited it to add any missed names (nicknames, invented fantasy/sci-fi terms).

---

## Phase 3 — Transform Functions (build + test each separately)
**Status:** ☐ not started

Test each sub-phase against `test_paragraph.txt` and read the output yourself before moving to the next. Do not combine these until all four work individually.

### 3.1 Synonym substitution
**Prompt to use:**
> "Write `src/transforms/synonym_sub.py` with a function `substitute_synonyms(text, protected_terms, swap_probability=0.15)`. Use spaCy for POS tagging, skip protected terms and function words (stopwords), and for eligible content words look up WordNet synonyms via NLTK, filtered to the same POS. Pick a synonym probabilistically (not always the first WordNet result) based on `swap_probability`. Return the modified text. Include a small test script that runs this on `test_paragraph.txt` and prints before/after."

### 3.2 Sentence splitting/merging
**Prompt to use:**
> "Write `src/transforms/sentence_reshape.py` with a function `reshape_sentences(text, split_probability=0.2, merge_probability=0.1)`. Use spaCy's dependency parse to find conjunction split-points in long sentences and split some of them probabilistically; also merge some short adjacent sentences with a connector. Return the modified text, preserving meaning. Include a test script against `test_paragraph.txt`."

### 3.3 Phrase-bank substitution
**Prompt to use:**
> "Write `src/transforms/phrase_bank.py`. Include a dictionary of common AI-typical transition phrases (e.g. 'moreover', 'furthermore', 'it is important to note', 'in conclusion', 'delve into') each mapped to a list of casual human alternatives. Write a function `substitute_phrases(text)` that finds these phrases (case-insensitive) and replaces each occurrence with a randomly chosen alternative from its list. Include a test script."

### 3.4 Noise injection
**Prompt to use:**
> "Write `src/transforms/noise.py` with a function `inject_noise(text, intensity=0.1)` that adds light, controlled human-like variation: occasional contraction of formal phrases ('it is' → 'it's'), occasional comma-to-em-dash swaps, and rare sentence fragments — all applied probabilistically based on `intensity`, never breaking grammar badly. Include a test script."

**Done when:** all four run individually on `test_paragraph.txt` and each output still reads coherently.

---

## Phase 4 — Humanness Scoring
**Status:** ☐ not started

**Goal:** a numeric score per paragraph estimating how "AI-typical" it still looks, no ML dependency required.

**Prompt to use:**
> "Write `src/scoring.py` with a function `humanness_score(text)` that returns a float 0-1. Compute: sentence length mean and standard deviation (higher stdev = more human, i.e. burstier), average word length, ratio of function words to content words, and count of remaining phrase-bank hits (import the phrase-bank dict from Phase 3.3). Combine these into a single weighted score — document the weights clearly as constants at the top of the file so they're easy to tune later. Include a test script that scores `test_paragraph.txt` before and after running it through the Phase 3 transforms."

**Done when:** the score visibly improves after transforms are applied on your test paragraphs.

*(Optional upgrade later, not required for v1): add local GPT-2-based perplexity scoring via `transformers` as an additional signal.*

---

## Phase 5 — Pipeline + Checkpointing
**Status:** ☐ not started

**Goal:** wire Phases 1-4 together with resumable, crash-safe processing for a full book.

**Prompt to use:**
> "Write `src/pipeline.py`. For each paragraph streamed from `stream_paragraphs` (Phase 1): apply the four Phase 3 transforms in sequence, then score with `humanness_score` (Phase 4). If score is below a threshold (default 0.6), re-run transforms once more with increased probabilities, capped at 3 total attempts. Immediately write the result to a checkpoint file (JSON lines format, one paragraph dict per line, in `checkpoints/`) as soon as it's processed — do not hold results in memory. Before starting, check `checkpoints/progress.json` for the last completed paragraph index and skip already-done work if the script is re-run. Use `tqdm` for a progress bar. Log which paragraphs got re-tried."

**Done when:** you can kill the script mid-run and re-running it resumes instead of restarting.

---

## Phase 6 — Reassembly
**Status:** ☐ not started

**Prompt to use:**
> "Write `src/reassemble.py` that reads the completed checkpoint JSONL file in paragraph order and stitches the text back into a single output file matching the original format (`.docx` with chapter headings preserved, or `.txt` with chapter markers), saved to `data/output/`."

**Done when:** output file opens cleanly and chapter structure matches the original book.

---

## Phase 7 — Manual QA (always do this, never skip)
**Status:** ☐ not started

No code prompt for this one — read actual output chapters yourself. Specifically check:
- Does it still sound like *your* book's voice, or generic?
- Any WordNet synonym swaps that read awkwardly? (Common failure point — tune `swap_probability` down if so.)
- Any character/place names that leaked through unprotected? (Add to `protected_terms.txt` and re-run just those paragraphs.)
- Any sentence splits that broke grammar? (Tune `split_probability` down.)

Tune the probability constants in Phases 3-5 based on this, then re-run affected chapters — checkpointing means you don't have to reprocess the whole book to fix one chapter.

---

## Working agreement for prompting your coding assistant

- One phase per conversation/prompt — don't ask for "the whole app" at once.
- Always paste the *exact* prompt text above; don't paraphrase it, since the specificity (function names, file paths, parameters) keeps output consistent across sessions.
- After each phase, actually run the test script before moving on — a phase that "looks right" but wasn't run is the #1 way vibe-coded projects silently break later.
- If a generated function doesn't match the spec above (wrong filename, wrong function signature), correct it in the same conversation before moving to the next phase — inconsistencies compound.