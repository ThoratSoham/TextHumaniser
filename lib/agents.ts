const OLLAMA_URL = "http://localhost:11434/api/generate";
const MODEL = "llama3.2:3b";

export async function askOllama(prompt: string): Promise<string> {
    const response = await fetch(OLLAMA_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            model: MODEL,
            prompt: prompt,
            stream: false,
            options: { temperature: 0.7 },
        }),
    });
    if (!response.ok) {
        throw new Error('Ollama problem: ${response.status}');
    }
    const data = await response.json();
    let answer: string = data.response;
    answer = answer.trim();
    answer = answer.replace(/^["']|["']$/g, "");
    return answer;
}

export async function simplify(text: string): Promise<string> {
    const prompt = [
    "Rewrite the following text using simple, plain words.",
    "Keep the meaning exactly the same.",
    "Use short sentences. Use everyday words.",
    "Do not add new information. Do not comment. Output ONLY the rewritten text.",
    "",
    "Text:",
    text,
  ].join("\n");
  return askOllama(prompt);
}

export async function adjustTone(
    text: string,
    repeated: { word: string; count: number }[]
): Promise<string> {
    const avoidList = repeated.map((r) => r.word).join(", ");
    const prompt = ["Rewrite the text below to sound warm and friendly.",
    "Use contractions like don't, it's, we're.",
    `Try to avoid repeating these words too much: ${avoidList}.`,
    "Keep the meaning exactly the same.",
    "Do not add new information. Do not comment. Output ONLY the rewritten text.",
    "",
    "Text:",
    text,
].join("\n");
return askOllama(prompt);
}

export async function finalPolish(text: string): Promise<string> {
    const prompt = [
    "Lightly clean up the text below.",
    "Fix capital letters at the start of sentences.",
    "Fix spacing mistakes (double spaces, missing spaces).",
    "Keep every word as close to the original as possible.",
    "Do not add new information. Do not comment. Output ONLY the cleaned text.",
    "",
    "Text:",
    text,
  ].join("\n");
  return askOllama(prompt);
}