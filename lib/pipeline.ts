import { analyzeText } from "./analyze";
import { applyRuleImprovements, splitLongSentences } from "./rules";
import { simplify, adjustTone, finalPolish } from "./agents";

export async function humanize(text: string): Promise<string> {
    const report = analyzeText(text);
    console.log("Analyser report:", report);

    let current = applyRuleImprovements(text);
    current = splitLongSentences(current, 25);
    
    current = await simplify(current);

    current = await adjustTone(current, report.repeated);

    current = await finalPolish(current);

    return current;
}