"""
src/ingest.py — streaming document reader.

Yields one paragraph at a time so a full book is never fully loaded into memory.
Supports .txt (double-newline-separated paragraphs, chapter detection via regex)
and .docx (python-docx paragraph objects, chapter detection via heading style).
"""

import re
from pathlib import Path
from typing import Iterator, Dict

import docx


DEFAULT_CHAPTER_REGEX = re.compile(r"^\s*chapter\b", re.IGNORECASE)


def _stream_txt(filepath: str, chapter_regex: re.Pattern) -> Iterator[Dict]:
    chapter = 0
    para_index = 0
    buffer = []

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()

            if stripped == "":
                if buffer:
                    text = " ".join(buffer).strip()
                    if text:
                        yield {"chapter": chapter, "para_index": para_index, "text": text}
                        para_index += 1
                    buffer = []
                continue

            if chapter_regex.match(stripped):
                # flush any pending buffer as a paragraph before starting new chapter
                if buffer:
                    text = " ".join(buffer).strip()
                    if text:
                        yield {"chapter": chapter, "para_index": para_index, "text": text}
                        para_index += 1
                    buffer = []
                chapter += 1
                para_index = 0
                # the chapter heading line itself is yielded as its own paragraph
                yield {"chapter": chapter, "para_index": para_index, "text": stripped}
                para_index += 1
                continue

            buffer.append(stripped)

        # flush remaining buffer at end of file
        if buffer:
            text = " ".join(buffer).strip()
            if text:
                yield {"chapter": chapter, "para_index": para_index, "text": text}


def _stream_docx(filepath: str) -> Iterator[Dict]:
    document = docx.Document(filepath)
    chapter = 0
    para_index = 0

    for para in document.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        style_name = (para.style.name or "").lower()
        is_heading = style_name.startswith("heading") or style_name == "title"

        if is_heading:
            chapter += 1
            para_index = 0
            yield {"chapter": chapter, "para_index": para_index, "text": text}
            para_index += 1
            continue

        yield {"chapter": chapter, "para_index": para_index, "text": text}
        para_index += 1


def stream_paragraphs(filepath: str, chapter_regex: re.Pattern = DEFAULT_CHAPTER_REGEX) -> Iterator[Dict]:
    """
    Generator yielding {chapter, para_index, text} dicts, one paragraph at a time.
    Supports .txt and .docx. Never loads the full document into memory at once.
    """
    ext = Path(filepath).suffix.lower()

    if ext == ".txt":
        yield from _stream_txt(filepath, chapter_regex)
    elif ext == ".docx":
        yield from _stream_docx(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}. Use .txt or .docx.")
