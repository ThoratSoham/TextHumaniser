#!/bin/bash
# create_issues.sh — creates one GitHub Issue per phase, with the real prompt in the body,
# and links each issue into your Project board.

REPO="ThoratSoham/TextHumaniser"     # change if your repo name differs
OWNER="ThoratSoham"
PROJECT_NUMBER=1

declare -A PHASE_BODIES=(
  ["Phase 0 — Environment Setup"]="Prompt: Set up a Python virtual environment for this project. Create a requirements.txt with: spacy, nltk, gensim, python-docx, tqdm. Write a setup.sh (or setup.py step) that installs requirements, downloads the spaCy en_core_web_sm model, and downloads the NLTK wordnet and omw-1.4 corpora. Then write a tiny test_setup.py that imports everything and parses one test sentence with spaCy to confirm it works."

  ["Phase 1 — Ingestion (streaming, big books)"]="Prompt: Write src/ingest.py. It should expose a generator function stream_paragraphs(filepath) that reads either a .txt or .docx file and yields one paragraph at a time (never the whole file into memory), each yielded as a dict: {chapter, para_index, text}. For .txt, split on double newlines and detect chapter breaks with a configurable regex (default: lines starting with 'Chapter'). For .docx, iterate paragraph objects with python-docx and use heading styles to detect chapter breaks. Include a test_ingest.py that runs this on a small sample file and prints the first 5 chunks."

  ["Phase 2 — Protected Terms Extraction"]="Prompt: Write src/protected_terms.py. It should read the full book (using stream_paragraphs from Phase 1), run spaCy NER over each paragraph, and collect all entities labeled PERSON, GPE, ORG, and NORP into a deduplicated set. Write the result, one term per line, to protected_terms.txt at the repo root. Also expose a function load_protected_terms() that other modules can import to get this set back as a Python set."

  ["Phase 3.1 — Synonym Substitution"]="Prompt: Write src/transforms/synonym_sub.py with a function substitute_synonyms(text, protected_terms, swap_probability=0.15). Use spaCy for POS tagging, skip protected terms and function words (stopwords), and for eligible content words look up WordNet synonyms via NLTK, filtered to the same POS. Pick a synonym probabilistically (not always the first WordNet result) based on swap_probability. Return the modified text. Include a small test script that runs this on test_paragraph.txt and prints before/after."

  ["Phase 3.2 — Sentence Splitting/Merging"]="Prompt: Write src/transforms/sentence_reshape.py with a function reshape_sentences(text, split_probability=0.2, merge_probability=0.1). Use spaCy's dependency parse to find conjunction split-points in long sentences and split some of them probabilistically; also merge some short adjacent sentences with a connector. Return the modified text, preserving meaning. Include a test script against test_paragraph.txt."

  ["Phase 3.3 — Phrase-Bank Substitution"]="Prompt: Write src/transforms/phrase_bank.py. Include a dictionary of common AI-typical transition phrases (e.g. 'moreover', 'furthermore', 'it is important to note', 'in conclusion', 'delve into') each mapped to a list of casual human alternatives. Write a function substitute_phrases(text) that finds these phrases (case-insensitive) and replaces each occurrence with a randomly chosen alternative from its list. Include a test script."

  ["Phase 3.4 — Noise Injection"]="Prompt: Write src/transforms/noise.py with a function inject_noise(text, intensity=0.1) that adds light, controlled human-like variation: occasional contraction of formal phrases ('it is' -> 'it's'), occasional comma-to-em-dash swaps, and rare sentence fragments — all applied probabilistically based on intensity, never breaking grammar badly. Include a test script."

  ["Phase 4 — Humanness Scoring"]="Prompt: Write src/scoring.py with a function humanness_score(text) that returns a float 0-1. Compute: sentence length mean and standard deviation (higher stdev = more human, i.e. burstier), average word length, ratio of function words to content words, and count of remaining phrase-bank hits (import the phrase-bank dict from Phase 3.3). Combine these into a single weighted score — document the weights clearly as constants at the top of the file so they're easy to tune later. Include a test script that scores test_paragraph.txt before and after running it through the Phase 3 transforms."

  ["Phase 5 — Pipeline + Checkpointing"]="Prompt: Write src/pipeline.py. For each paragraph streamed from stream_paragraphs (Phase 1): apply the four Phase 3 transforms in sequence, then score with humanness_score (Phase 4). If score is below a threshold (default 0.6), re-run transforms once more with increased probabilities, capped at 3 total attempts. Immediately write the result to a checkpoint file (JSON lines format, one paragraph dict per line, in checkpoints/) as soon as it's processed — do not hold results in memory. Before starting, check checkpoints/progress.json for the last completed paragraph index and skip already-done work if the script is re-run. Use tqdm for a progress bar. Log which paragraphs got re-tried."

  ["Phase 6 — Reassembly"]="Prompt: Write src/reassemble.py that reads the completed checkpoint JSONL file in paragraph order and stitches the text back into a single output file matching the original format (.docx with chapter headings preserved, or .txt with chapter markers), saved to data/output/."

  ["Phase 7 — Manual QA"]="No code prompt for this one — read actual output chapters yourself. Check: Does it still sound like your book's voice, or generic? Any WordNet synonym swaps that read awkwardly? Any character/place names that leaked through unprotected? Any sentence splits that broke grammar? Tune the probability constants in Phases 3-5 based on this, then re-run affected chapters."
)

for title in "${!PHASE_BODIES[@]}"; do
  echo "Creating issue: $title"
  issue_url=$(gh issue create --repo "$REPO" --title "$title" --body "${PHASE_BODIES[$title]}")
  echo "  -> $issue_url"
  gh project item-add "$PROJECT_NUMBER" --owner "$OWNER" --url "$issue_url"
done

echo "Done. Run 'gh project view $PROJECT_NUMBER --owner $OWNER --web' to see the board."