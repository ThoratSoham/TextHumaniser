import { countWords } from "./analyze";

const PHRASE_SWAPS: [string, string[]][] = [
  ["in conclusion", ["so, to wrap up", "all in all", "to sum this up"]],
  ["it is important to note that", ["keep in mind", "note that", "here's the thing:"]],
  ["utilize", ["use", "use", "work with"]],
  ["commence", ["start", "begin", "kick off"]],
  ["prior to", ["before", "before", "ahead of"]],
  ["subsequently", ["then", "after that", "next"]],
  ["in the event that", ["if", "if", "when"]],
  ["a large number of", ["many", "lots of", "plenty of"]],
  ["due to the fact that", ["because", "since", "as"]],
];

const CONTRACTIONS: [string, string][] = [
  [" do not ", " don't "],
  [" does not ", " doesn't "],
  [" did not ", " didn't "],
  [" cannot ", " can't "],
  [" will not ", " won't "],
  [" is not ", " isn't "],
  [" are not ", " aren't "],
  [" it is ", " it's "],
  [" that is ", " that's "],
  [" there is ", " there's "],
  [" we are ", " we're "],
  [" you are ", " you're "],
  [" they are ", " they're "],
];

export function applyRuleImprovements(text: string): string {
    let result = text;

    for (const [phrase, options] of PHRASE_SWAPS){
        const pattern = new RegExp(phrase, "gi");
        result = result.replace(pattern, () => {
            const pick = Math.floor(Math.random() * options.length);
            return options[pick];
        });
    }

    for (const [long, short] of CONTRACTIONS) {
        result = result.split(long).join(short);
    }

    return result;
}

export function splitLongSentences(text: string, maxWords: number): string {
    const sentences = text.replace(/([.!?])\s+/g, "$1|").split("|");
    const fixed = sentences.map((sentence) => {
        const trimmed = sentence.trim();
        if (countWords(trimmed) <= maxWords) return trimmed;
        const breakPoints = [", and ", ", but ", ", so ", "; "];
        for (const bp of breakPoints) {
            const idx = trimmed.indexOf(bp);
            if (idx > 0) {
                const first = trimmed.slice(0, idx) + ".";
                const second = trimmed.slice(idx + bp.length);
                const capitalized = second.charAt(0).toUpperCase() + second.slice(1);
                return first + " " + capitalized;
            }
        }
        return trimmed;
    });
    return fixed.join(" ");
}