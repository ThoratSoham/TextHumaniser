export function countWords(text: string): number {
    const words = text.trim().split(/\s+/);
    if (words[0] === "") return 0;
    return words.length;
}

export function splitSentences(text: string): string[] {
    const parts = text
        .replace(/([.!?])\s+/g, "$1|")
        .split("|")
        .map((s) => s.trim())
        .filter((s) => s.length > 0);
    return parts;
}

export function countSentences(text: string): number {
    return splitSentences(text).length;
}

export function averageSentenceLength(text: string): number {
    const sentences = splitSentences(text);
    if (sentences.length === 0) return 0;
    const totalWords = sentences.reduce((sum, s) => sum + countWords(s), 0);
    return totalWords / sentences.length;
}

export function sentenceLengthVariance(text: string): number {
    const lengths = splitSentences(text).map((s)=> countWords(s));
    if (lengths.length < 2) return 0;
    const mean = lengths.reduce((a,b) => a + b, 0) / lengths.length;
    const squaredDiffs = lengths.map((n) => (n - mean) * (n - mean));
    const variance = squaredDiffs.reduce((a,b) => a+b, 0) / squaredDiffs.length;
    return variance;
}

export function topRepeatedWords(text: string, count: number): {word: string; count: number}[] {
    const STOP_WORDS = new Set([ "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "is", "are", "was", "were", "be", "been", "it", "this",
    "that", "as", "by", "from", "i", "you", "he", "she", "we", "they",
    "my", "your", "his", "her", "our", "their", "not", "no", "so", "if",
    "then", "than", "there", "here", "what", "which", "who", "do", "does",
    "did", "have", "has", "had", "will", "would", "can", "could", "should",
  ]);

  const words = text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, "")
    .split(/\s+/)
    .filter((w) => w.length > 0 && !STOP_WORDS.has(w));
  const counts = new Map<string, number>();
  for (const w of words) {
    const current = counts.get(w) ?? 0;
    counts.set(w, current + 1);
  }
  const sorted = [...counts.entries()].sort((a,b) => b[1] - a[1]);
  return sorted.slice(0, count).map(([word, n]) => ({ word, count: n}));
}

export function analyzeText(text: string) {
    return {
        words: countWords(text),
        sentences: countSentences(text),
        avgSentenceLength: averageSentenceLength(text);
        variance: sentenceLengthVariance(text),
        repeated: topRepeatedWords(text, 5),
    };
}