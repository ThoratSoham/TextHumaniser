#!/bin/bash
# create_project.sh — sets up the Book Humanizer project board via GitHub CLI

REPO="https://github.com/ThoratSoham/TextHumaniser"   # change this
OWNER="ThoratSoham"                  # change this

# 1. Create the project (returns a project number)
gh project create --owner "$OWNER" --title "Book Humanizer Build"

# Note the project NUMBER printed above, then set it here:
PROJECT_NUMBER=1   # change to whatever number was returned

# 2. Add one item per phase
PHASES=(
  "Phase 0 — Environment Setup"
  "Phase 1 — Ingestion (streaming, big books)"
  "Phase 2 — Protected Terms Extraction"
  "Phase 3.1 — Synonym Substitution"
  "Phase 3.2 — Sentence Splitting/Merging"
  "Phase 3.3 — Phrase-Bank Substitution"
  "Phase 3.4 — Noise Injection"
  "Phase 4 — Humanness Scoring"
  "Phase 5 — Pipeline + Checkpointing"
  "Phase 6 — Reassembly"
  "Phase 7 — Manual QA"
)

for phase in "${PHASES[@]}"; do
  gh project item-create "$PROJECT_NUMBER" --owner "$OWNER" --title "$phase"
done

echo "Done. Run 'gh project view $PROJECT_NUMBER --owner $OWNER --web' to open it."