"""
test_ingest.py — verifies src/ingest.py streams a sample document correctly.
"""

from src.ingest import stream_paragraphs


def main():
    filepath = "data/input/sample_book.txt"
    print(f"Streaming: {filepath}\n")

    count = 0
    for chunk in stream_paragraphs(filepath):
        print(f"[ch {chunk['chapter']} / para {chunk['para_index']}] {chunk['text'][:80]}")
        count += 1
        if count >= 10:
            break

    print(f"\nTotal chunks printed: {count}")


if __name__ == "__main__":
    main()
