#!/bin/bash
# setup.sh — one-time environment setup for TextHumaniser
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Downloading spaCy English model (small, ~50MB)..."
python -m spacy download en_core_web_sm

echo "Downloading NLTK WordNet corpora..."
python -c "import nltk; nltk.download('wordnet'); nltk.download('omw-1.4')"

echo ""
echo "Setup complete. Run 'python test_setup.py' to verify."
