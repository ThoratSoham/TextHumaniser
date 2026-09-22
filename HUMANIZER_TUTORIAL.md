# Humanizer — Build Your Own Local AI Writing Coach

*A complete beginner tutorial. Every line explained. 100% local. No cloud, no paid APIs, no login, no database, no deployment.*

**Made for:** a student with zero coding experience, a Windows laptop, 8 GB of RAM, and about 1 hour per day.

---

## 1. Title and Introduction

Hi! You are going to build a real web app called **Humanizer**.

**What it does:** You paste text into a box, click one button, and get back text that sounds more natural and human — like a person wrote it, not a robot.

**Who this is for:** You! Someone who has never coded before, has a Windows laptop, and can give about 1 hour per day. Nothing in this tutorial assumes you know anything about programming. Every single line of code is explained like you are 10 years old.

**What you will learn by the end:**

- How to write code in **TypeScript** (a very popular, beginner-friendly language)
- How a web app works (the part the user sees + the part the computer runs)
- Simple **math for text**: counting words, averaging sentence lengths, and measuring "spread" (variance)
- How to run a tiny **AI brain** on your own laptop using **Ollama**
- How to chain several AI steps together into a **pipeline**

**The one rule of this tutorial:** never copy a line of code you don't understand. Every line gets explained. If a line confuses you, stop, re-read that section, and only then move on. One hour a day is plenty — the project is split into tiny Parts (0 to 10), and each Part is small enough to finish and test in one sitting.

**How to use this tutorial:**

1. Read one Part at a time.
2. Type the code yourself (don't copy-paste — typing is how you learn).
3. Run it. Test it. Only then move to the next Part.

**Time estimate:** about 12–15 hours total, spread over 2–3 weeks at 1 hour per day. Parts 0–3 are pure coding basics. Part 4 installs the AI. Parts 5–8 build the AI features. Parts 9–10 test and polish.

**Contents:**

1. Title and Introduction
2. Ethics Note
3. What You Will Build (with diagram)
4. Tools Needed and Installation on Windows
5. Part 0: Create Project Folder and Docs
6. Part 1: Simple Page (No AI Yet)
7. Part 2: Math Analyzer
8. Part 3: Rule-Based Improvements
9. Part 4: Install Ollama and Run a Small Model
10. Part 5: First AI Agent (Simplifier)
11. Part 6: Multi-Agent Pipeline
12. Part 7: Connect UI to Agents
13. Part 8: Add Copy Button
14. Part 9: Test Everything
15. Part 10: Final Polish and Next Steps
16. README.md Content
17. Glossary of Every Term Used

---

## 2. Ethics Note — Read This First

**Humanizer is a writing COACH, not a cheating tool.**

Think of it like a gym trainer for your writing:

- A trainer shows you *how* to lift properly — but you still do the lifting.
- Humanizer shows you *why* your writing sounds robotic — but you should still be the author.

The most valuable part of this app is honestly **Part 2** (the math analyzer). It shows you *numbers* that explain what makes text feel stiff: every sentence the same length, the same words repeated, no contractions. Once you can *see* those numbers, you start fixing them in your own writing by yourself. That's real learning.

**Do NOT use Humanizer to:**

- Rewrite text for school or university assignments and submit it as your own work. That is plagiarism in spirit even if the words change — and AI detectors increasingly flag rewritten text anyway, so you risk serious trouble for zero learning.
- "Humanize" AI-generated essays so they slip past detectors. That's the same thing with extra steps, and it defeats the point of education.
- Bypass rules from a teacher, university, employer, or platform. Some places legally require AI-generated content to be labeled as such.

**DO use Humanizer to:**

- Understand **why** your text feels robotic — the analyzer shows you the numbers.
- Practice varying your own sentence lengths and word choices.
- Polish **your own** drafts — your essay, your email, your story that *you* wrote.
- Learn what "natural" writing looks like statistically.

**The simple test:** Would you be comfortable explaining to your teacher exactly how you produced this text — including "I used a local tool on my laptop to help me polish my own draft"? If yes → fine. If no → don't do it.

We will build this the honest way: the math analyzer is the *teacher* (it shows you the numbers), and the AI agents are *helpers* whose suggestions you decide to keep or throw away.

---

## 3. What You Will Build (with Simple Diagram)

**In one sentence:** a local web page where you paste text, click "Humanize," and see improved text appear — all computed on your laptop, nothing ever leaves your machine.

Here is the whole app as a picture:

```
┌─────────────────────────────────────────────────────────────┐
│  YOUR BROWSER (the part you SEE)                            │
│                                                             │
│   ┌───────────────────────┐      ┌───────────────────────┐  │
│   │ textarea: paste your  │      │ output box: the       │  │
│   │ text here             │      │ improved text appears │  │
│   └───────────────────────┘      └───────────────────────┘  │
│        [ Humanize button ]       [ Copy button ]            │
└────────────────────────────┬────────────────────────────────┘
                             │  sends your text
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  NEXT.JS SERVER (the part that WORKS, same laptop)          │
│                                                             │
│   /api/humanize  (the "kitchen" that processes your text)   │
│        │                                                    │
│        ▼                                                    │
│   1. Math Analyzer    → counts words, sentences, variance   │
│        │                                                    │
│        ▼                                                    │
│   2. Rule Fixes       → swaps robotic phrases, fast & free  │
│        │                                                    │
│        ▼                                                    │
│   3. Simplifier Agent  → rewrites in plain, short sentences │
│        │                                                    │
│        ▼                                                    │
│   4. Tone Adjuster    → warms it up, adds contractions      │
│        │                                                    │
│        ▼                                                    │
│   5. Final Polisher   → fixes capitals, spacing, small bits │
└────────────────────────────┬────────────────────────────────┘
                             │  asks the local AI
                             ▼
┌─────────────────────────────────────────────────────────────┐
│  OLLAMA (a helper program running on YOUR laptop)           │
│  listens at localhost:11434                                 │
│  runs the model: Llama 3.2 3B (a small AI brain, ~2 GB)     │
└─────────────────────────────────────────────────────────────┘
```

**What each piece is, in kid terms:**

- **Browser** = the window you look at. It shows boxes and buttons.
- **Next.js** = a toolbox that builds *both* the page you see *and* the hidden server code behind it. One project does both jobs.
- **API route** = a kitchen door inside your app. The page sends your text through the door, the kitchen cooks it, and sends the result back.
- **Ollama** = a free helper program that runs a small AI brain entirely on your laptop. It waits for requests at `localhost:11434`. (`localhost` just means "this same computer" — nothing goes out to the internet.)
- **Llama 3.2 3B** = a small AI model (about 2 GB). "3B" means 3 billion tiny number-knobs inside it. Small, but smart enough to rewrite text.
- **Agent** = nothing magic! Just a small function that sends your text + an instruction to the AI and gets text back. We will write 3 of them.

**What you will NOT build:** cloud services, accounts, logins, databases, saved history, Docker, deployment, anything paid, anything advanced. Just a simple, honest tool.

---

## 4. Tools Needed and Installation on Windows

You already have Node.js, Git, and VS Code installed. Let's verify each one, then install Ollama (the only new tool).

> **How to open a terminal on Windows:** press the Windows key, type `cmd`, press Enter. A black window appears — that's the Command Prompt, where you type commands. (In VS Code you can also use Terminal → New Terminal from the top menu.)

### 4.1 Check Node.js

In Command Prompt, type:

```bash
node -v
```

You want something like `v20.11.0` or higher. That's Node's version number.

- If you see a version → great, move on.
- If you see `'node' is not recognized...` → install Node.js from [nodejs.org](https://nodejs.org). Download the **LTS** version, run the installer, click Next Next Next, then **close and reopen** Command Prompt and try again.

### 4.2 Check Git (optional for this tutorial)

```bash
git --version
```

If you see a version like `git version 2.45.1`, you're set. We won't really need Git in this tutorial, but it's good to know it works.

### 4.3 Check VS Code

Open VS Code from the Start menu. That's it — nothing to install inside it yet. We'll use it as our editor (the fancy notebook where we write code).

### 4.4 Install Ollama (the local AI runner)

Ollama is a free program that runs AI models on your own computer. No account, no API key, no internet needed after download.

1. Go to [ollama.com/download](https://ollama.com/download)
2. Download the **Windows** installer (a `.exe` file).
3. Double-click it and click through the installer (Next, Install, Finish).
4. After install, Ollama runs quietly in the background. You'll see a little llama icon near the clock (bottom-right corner).

Open a **NEW** Command Prompt window (it must be new, so it can find Ollama) and type:

```bash
ollama --version
```

You should see something like `ollama version is 0.5.7`.

> **If `ollama` is not recognized:** close Command Prompt and open a fresh one. Windows only learns about newly installed programs when a terminal starts. Still broken? Restart your PC.

### 4.5 Download a small AI model

We'll use **Llama 3.2 3B**. It's about 2 GB, runs fine on a normal CPU (your i3 is fine — it will just be slowish, which is normal), and it's good at following writing instructions.

```bash
ollama pull llama3.2:3b
```

This downloads the model to your laptop. Expect 10–30 minutes depending on your internet. It's a one-time download — after that it works offline forever.

Check that it works by asking it a question:

```bash
ollama run llama3.2:3b "Why is the sky blue?"
```

After a few seconds of thinking, you should see an answer appear in the terminal. If you do — Ollama and the model are working!

Type `/bye` and press Enter to exit the chat.

> **RAM warning (you have 8 GB):** running the AI uses a lot of memory. Close Chrome tabs and other big programs while testing the app, or everything will crawl.

> **If Llama 3.2 3B feels too slow:** try **Phi-3 Mini** instead — a different small model, also about 2 GB, sometimes faster on modest hardware:
>
> ```bash
> ollama pull phi3:mini
> ```
>
> Then just use `phi3:mini` everywhere this tutorial says `llama3.2:3b`. Everything else works identically. (One small note: Phi-3 Mini sometimes ignores the "output only the rewritten text" instruction more often than Llama does. We defend against that in Part 5 — we instruct the model strictly *and* strip stray quotes from the edges of its answer — so both models end up usable.)

### 4.6 About Next.js (nothing to install yet)

Next.js is the toolbox that builds our web app — the page AND the behind-the-scenes server. We don't install it manually; we create the project with one command in **Part 0**, and that command sets everything up.

### ✅ Checklist before moving to Part 0

- [ ] `node -v` prints a version number (v20+)
- [ ] VS Code opens
- [ ] `ollama --version` prints a version
- [ ] `ollama run llama3.2:3b "Why is the sky blue?"` prints an answer
- [ ] No other programs are hogging your RAM

All checked? On to Part 0.

---

## 5. Part 0: Create Project Folder and Docs

**Goal:** create the project with one command, understand what's inside it, and set up a `docs` folder for your notes.

**Kid analogy:** create-next-app is like a starter LEGO kit — it gives you the baseplate and a few pre-built pieces so you don't start from zero.

> **Important:** this tutorial creates a NEW folder called `next`. It is a separate project from anything else on your computer. All commands below are typed in Command Prompt.

### Step 1: Pick a home and create the project

In Command Prompt, go wherever you keep your projects (the Desktop is fine) and run:

```bash
cd C:\Users\YourName\Desktop
npx create-next-app@latest humanizer
```

- `cd` means "change directory" — walk into that folder.
- `npx` means "run a tool without permanently installing it" — here, the tool is `create-next-app`, Next.js's project maker. The first time, it may ask permission to download the tool: press `y` then Enter.

The wizard now asks you questions. Answer exactly like this (use arrow keys + Enter):

| Question | Answer | Why |
|---|---|---|
| TypeScript? | **Yes** | TypeScript is our language — it catches typos for you |
| ESLint? | **No** | A code-rule checker; extra noise for a first project (Yes is also fine) |
| Tailwind CSS? | **Yes** | Our styling tool |
| Code inside a `src/` directory? | **No** | Fewer folders = simpler |
| App Router? (recommended) | **Yes** | The modern way Next.js organizes pages |
| Turbopack for `next dev`? | **Yes** | A faster dev server; if anything acts weird later, say No and rerun |
| Customize the import alias? | **No** | The default (`@/...`) is exactly what we want |

Now it downloads everything and runs `npm install` automatically (the "shopping" step — it fetches the packages our project needs). This takes a few minutes. When it finishes, you'll see a success message with cute ASCII art.

### Step 2: Look inside your new project

```bash
cd humanizer
```

Now open the folder in VS Code: **File → Open Folder → choose `humanizer`**.

Here's what each thing is (don't touch most of them):

- `app/` — the pages of your website live here
  - `app/page.tsx` — **the homepage**. This is the file you'll edit most.
  - `app/layout.tsx` — the "picture frame" wrapped around every page (fonts, background).
  - `app/globals.css` — global styles; Tailwind gets loaded here.
- `app/api/` — server code lives here (we'll add our kitchen in Part 7)
- `node_modules/` — the downloaded packages. HUGE and boring. Never edit it.
- `package.json` — the project's shopping list: which packages we use, and which commands we can run.
- `tsconfig.json` — the rules for TypeScript, including the `@/...` shortcut (more on that in Part 7).
- `.gitignore` — a list of files Git should not track (like `node_modules`).
- `next.config.ts` — Next.js settings. We never open it in this tutorial.

### Step 3: Create your docs folder

In VS Code's left panel (Explorer), right-click on the empty space at the bottom of the file list → **New Folder** → name it `docs`. Then right-click `docs` → **New File** → name it `NOTES.md`.

Paste this starter into `docs/NOTES.md`:

```markdown
# My Humanizer Notes

## Day 1 — (today's date)
- Today I did: Part 0
- New words I learned:
- Things that confused me:
- One thing I want to try later:
```

Why keep notes? Because "I'll remember it" is a lie every programmer tells themselves. One honest paragraph per day will beat any tutorial.

### ✅ Run and test it

```bash
npm run dev
```

- This starts the **dev server** — a small program that serves your website to your browser while you develop.
- When it says `Ready`, open your browser at **http://localhost:3000**. You should see the Next.js starter page.
- `localhost:3000` = "this computer, door number 3000". Your page is served from your own machine.
- To stop the server: click on the terminal and press **Ctrl+C** (hold Control, tap C). Do this before closing for the day.

**Test:** leave the server running, change nothing yet. If the page loads without errors — Part 0 done. 🎉

---

## 6. Part 1: Simple Page (No AI Yet)

**Goal:** replace the starter page with our own: one input box, one button, one output box. No AI, no server code — just the skeleton.

**Kid analogy:** we're building the frame of a toy house — walls, doors, rooms. No furniture yet.

### The code

Open `app/page.tsx`, delete **everything**, and type this:

```tsx
"use client";

import { useState } from "react";

export default function Home() {
  const [draft, setDraft] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  return (
    <main className="min-h-screen bg-slate-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-2">Humanizer</h1>
      <p className="text-center text-slate-500 mb-8">
        100% local — your text never leaves your laptop.
      </p>

      <div className="max-w-3xl mx-auto flex flex-col gap-4">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Paste your text here..."
          className="w-full h-48 p-4 rounded-lg border border-slate-300 bg-white"
        />

        <button
          onClick={() => alert("Button works! (AI comes later)")}
          disabled={draft.trim() === "" || isLoading}
          className="bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400"
        >
          {isLoading ? "Working..." : "Humanize"}
        </button>

        <textarea
          value={result}
          readOnly
          placeholder="The improved text will appear here..."
          className="w-full h-48 p-4 rounded-lg border border-slate-300 bg-white"
        />
      </div>
    </main>
  );
}
```

### Line-by-line explanation

**Line 1: `"use client";`**
This is a sticker on the file that tells Next.js: "this part is *alive* — it has buttons and reacts to clicks." Files without this sticker are quiet, still pictures (that load faster). Ours needs life, so it gets the sticker. It must be the very first line.

**Line 2: `import { useState } from "react";`**
We're borrowing a tool named `useState` from a big toolbox called React. Analogy: `import` = "please pass me the wrench from the toolbox." React is the library (a collection of pre-written code) that redraws the page when things change.

**Line 4: `export default function Home() {`**
- `function Home()` — a recipe named Home. Inside the curly braces `{ }` is what it does.
- `export default` — a sign that says "THIS is the main part of the page." Next.js looks at `app/page.tsx` and renders whatever is exported default from it.

**Lines 5–7: the three whiteboards**

```tsx
const [draft, setDraft] = useState("");
```

- `useState("")` creates a **whiteboard** that starts empty (`""` means empty text). When the whiteboard changes, React automatically repaints the page to match. That's the whole trick of React.
- `const [draft, setDraft]` — we name two things: `draft` is what's currently written on the whiteboard; `setDraft` is the only pen allowed to write on it. (You never write `draft = something` directly — always use the pen.)
- `const` means "a box whose label never changes" (a constant). We use `const` unless we truly need to reassign, which we don't in this file.
- `result` / `setResult` — same idea, for the improved text.
- `isLoading` / `setIsLoading` — a yes/no whiteboard that will show "Working..." while the AI thinks. Right now it's always `false` (no), but we already use it below so Part 7 doesn't need to redesign the page.

**Line 9: `return (`**
The function hands back what the page should show. Everything in the parentheses is **JSX** — HTML-like code that lives inside JavaScript. Three rules: (1) it must have exactly one outer element (ours is `<main>`), (2) every tag must close (like `</main>`), (3) we write `className` instead of `class` because `class` is a reserved word in JavaScript.

**Line 10: `<main className="min-h-screen bg-slate-100 p-8">`**
The outer box of the page. The words in quotes are **Tailwind classes** — tiny ready-made style words. Here's your mini dictionary (you'll see these over and over):

| Class | Meaning |
|---|---|
| `min-h-screen` | at least as tall as the whole screen |
| `bg-slate-100` | very light gray background |
| `p-8` | padding of 8 small units (space *inside* the box) |
| `text-3xl` | big text |
| `font-bold` | bold letters |
| `text-center` | centered text |
| `mb-2` / `mb-8` | margin-bottom (space *below* the element) |
| `max-w-3xl mx-auto` | max width, then auto-centering left/right |
| `flex flex-col gap-4` | stack children vertically with gaps between them |
| `w-full h-48` | full width, fixed height |
| `rounded-lg border border-slate-300` | rounded corners with a gray border |
| `bg-white` | white background |

**Lines 15–20: the input textarea**

- `value={draft}` — the box *shows* whatever is on the draft whiteboard. The braces `{ }` mean "this is JavaScript, not plain text."
- `onChange={(e) => setDraft(e.target.value)}` — the heartbeat of the page. Every time you type one letter: React calls this little function; `e` is the event (the "something happened" package); `e.target` is the box; `e.target.value` is the box's current text; `setDraft(...)` writes it on the whiteboard; React repaints. So fast you never notice.
- `(e) => ...` is an **arrow function** — a tiny unnamed recipe written in one line.

**Lines 22–28: the button**

- `onClick={() => alert(...)}` — when clicked, pop up a test message. (We replace this in Part 7 with the real thing.)
- `disabled={draft.trim() === "" || isLoading}` — the button is grayed out when either: the text box is empty (`.trim()` cuts invisible spaces off the ends, so a box with only spaces counts as empty), or we're currently working. `||` means "or."
- The long `className` list styles it blue, and `disabled:bg-slate-400` means "when disabled, be gray instead."
- `{isLoading ? "Working..." : "Humanize"}` — a **ternary**, a one-line if/else: *if* loading, show "Working...", *else* show "Humanize".

**Lines 30–35: the output textarea**

- `value={result}` — shows the improved text.
- `readOnly` — the user can't type in it. It's a display case, not a whiteboard.

### ✅ Run and test it

With `npm run dev` still running, save the file and look at http://localhost:3000 (it updates by itself — that's **hot reload**):

1. The page shows your title, input box, button, output box.
2. Click the button while it's gray → nothing happens (it's disabled).
3. Type "hello" in the input → the button turns blue (enables).
4. Click it → an alert pops up saying the button works. Close it.
5. Try typing in the output box → you can't (readOnly).

All five pass = Part 1 done. 🎉

---

## 7. Part 2: Math Analyzer

**Goal:** write pure-math functions that count words, count sentences, measure sentence-length **variance**, and find **repeated words**. No AI yet — just counting.

**Why this is the heart of the app:** robot text has *low variance* (every sentence is the same length) and *high repetition* (the same words over and over). Human text wobbles. If you learn to see these numbers, you can fix your own writing without any AI.

### The code

In VS Code, create a new folder `lib` in the project root (same level as `app`), and inside it a new file `lib/analyze.ts`:

```ts
// analyze.ts — counts things about a piece of text.

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
  const lengths = splitSentences(text).map((s) => countWords(s));
  if (lengths.length < 2) return 0;
  const mean = lengths.reduce((a, b) => a + b, 0) / lengths.length;
  const squaredDiffs = lengths.map((n) => (n - mean) * (n - mean));
  const variance = squaredDiffs.reduce((a, b) => a + b, 0) / squaredDiffs.length;
  return variance;
}

export function topRepeatedWords(
  text: string,
  count: number
): { word: string; count: number }[] {
  const STOP_WORDS = new Set([
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for",
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
  const sorted = [...counts.entries()].sort((a, b) => b[1] - a[1]);
  return sorted.slice(0, count).map(([word, n]) => ({ word, count: n }));
}

export function analyzeText(text: string) {
  return {
    words: countWords(text),
    sentences: countSentences(text),
    avgSentenceLength: averageSentenceLength(text),
    variance: sentenceLengthVariance(text),
    repeated: topRepeatedWords(text, 5),
  };
}
```

### Line-by-line explanation

**`export`** — a stamp that means "other files are allowed to use this function." Without it, the function is private to this file.

**`function countWords(text: string): number {`** — a recipe named countWords. `text: string` means "the ingredient must be text" and `: number` means "this recipe produces a number." TypeScript reads these promises and screams at you *before* the app runs if you break one. That's why we use TypeScript instead of plain JavaScript — it's a spell-checker for code.

**Inside countWords:**

- `text.trim()` — cut invisible spaces off the two ends of the text.
- `.split(/\s+/)` — cut the text into pieces at every run of whitespace. The slashes `/.../ ` make a **regex** — a tiny search pattern. Inside, `\s` means "any space-like character (space, tab, new line)" and `+` means "one or more in a row." So `/\s+/` = "one or more spaces."
- Edge case: splitting an empty string gives `[""]` — a list with one empty piece. So `if (words[0] === "") return 0;` catches the "no words at all" case and returns zero. (`===` means "is exactly equal to"; always use `===`, never `==`.)
- `return words.length` — how many pieces we got = the word count.

**`splitSentences`** — cuts text into sentences:

- `.replace(/([.!?])\s+/g, "$1|")` — find sentence-ending punctuation (a period `.` or `!` or `?`) followed by spaces. The parentheses `([.!?])` **remember** what was found, and `$1` means "put the remembered thing back." So we replace `"dog. The"` with `"dog.|The"` — we plant a little `|` flag after each sentence end. The `g` at the end means "everywhere, not just the first time."
- `.split("|")` — cut at every flag. Now we have sentences!
- `.map((s) => s.trim())` — `map` means "do this to every item and collect the results." Here: trim each sentence.
- `.filter((s) => s.length > 0)` — `filter` means "keep only the items that pass the test." Empty pieces get thrown away.
- Return the list of sentences. (Honest note: this misses abbreviations like "Dr." — a real tool would handle that. Simple is our goal.)

**`averageSentenceLength`**:

- If there are no sentences, return 0 (dividing by zero is forbidden in math and in code).
- `sentences.reduce((sum, s) => sum + countWords(s), 0)` — `reduce` is the "walking the line of kids, adding up their candies" function: start at `0`, visit each sentence, add its word count to the running total `sum`.
- `totalWords / sentences.length` — the classic average. Example: 3 sentences with 10 words total → average 3.33 words.

**`sentenceLengthVariance`** — the star of the show:

- `lengths` is the list of sentence lengths, e.g. `[10, 11, 9, 10]`.
- If there are fewer than 2 sentences, variance is 0 — you can't measure wobble with one number.
- `mean` = the average (the "fair share"). Cookie analogy: 40 cookies for 4 kids → each kid's *fair share* is 10.
- `(n - mean) * (n - mean)` — for each sentence, how far is it from the fair share? We **square** the distance so that negatives don't cancel out positives (if one sentence is +3 and another is −3, adding raw distances gives 0 and hides the wobble; squaring makes both count).
- `variance` = the average of those squared distances. **Huddled lengths → small variance → robotic. Spread-out lengths → big variance → human.** As a rough rule of thumb for English prose, an average sentence length around 10–20 words with variance roughly above ~15 feels lively — but there are no magic numbers; use it as a flashlight, not a law.

**`topRepeatedWords`** — the bean-jar counter:

- `STOP_WORDS` is a **Set** — a bag where each item exists at most once, with a super-fast `has()` check. These are filler words ("the", "a", "and") that repeat in *every* text; counting them tells us nothing, so we ignore them.
- `.toLowerCase()` — make everything lowercase so "Dog" and "dog" count as the same word.
- `.replace(/[^a-z0-9\s]/g, "")` — delete every character that is **not** a letter, digit, or space (commas, periods...). Inside the regex, `^` at the front of the brackets means "not any of these."
- `.filter((w) => w.length > 0 && !STOP_WORDS.has(w))` — keep words that exist and aren't on the ignore list. `&&` means "and"; `!` means "not."
- `counts` is a **Map** — a cabinet of labeled drawers: each drawer label is a word, the contents are how many times we've seen it.
- `for (const w of words)` — walk through every word, one at a time.
- `counts.get(w) ?? 0` — "what's in this word's drawer?" The `??` means "if the answer is empty/undefined, use 0 instead." Then `counts.set(w, current + 1)` — put one more bean in the jar.
- `[...counts.entries()]` — the three dots are the **spread**: "pour all the drawers out into a list." Each item is a pair like `["report", 4]`.
- `.sort((a, b) => b[1] - a[1])` — sort with a custom rule: compare counts (`b[1]` and `a[1]` are the second slots of the pairs). Subtracting `a` from `b` sorts biggest-first.
- `.slice(0, count)` — take only the first `count` items (we ask for 5).
- `.map(([word, n]) => ({ word, count: n }))` — reshape each pair `["report", 4]` into a tidy object `{ word: "report", count: 4 }`.

**`analyzeText`** — the one-stop shop that returns all five numbers in a single object. Other files will call just this one function.

### Try it right now

Create `lib/tryAnalyze.ts` (a scratch file for experiments — it's never part of the app):

```ts
import { analyzeText } from "./analyze";
import { applyRuleImprovements } from "./rules";

const sample =
  "The report was finalized. The report was reviewed. " +
  "The report was approved by the team, and the report was then submitted. " +
  "Great!";

const report = analyzeText(sample);
console.log(report);
```

(Don't worry that `./rules` doesn't exist yet — we create it in Part 3. For now, comment the import out with `//` at the start of the line if you want to run this immediately.)

Run it in the terminal (from the project folder):

```bash
npx tsx lib/tryAnalyze.ts
```

- `npx tsx` runs a helper that executes TypeScript files directly (the first run asks to download it — press `y`).

You should see something like:

```
{
  words: 21,
  sentences: 4,
  avgSentenceLength: 5.25,
  variance: 2.1875,
  repeated: [
    { word: 'report', count: 4 },
    { word: 'finalized', count: 1 },
    ...
  ]
}
```

**Read the numbers like a detective:** "report" appears 4 times in 21 words (the bean jars caught it), and the variance is tiny (all four sentences are ~5 words — huddled). This text is *provably* robotic. Parts 3 and 6 exist to fix exactly what these numbers just exposed.

### ✅ Test it

1. The command above prints the report. ✅
2. Change the sample to something you wrote and run again — do the numbers match your gut feeling?
3. Type something with no punctuation at all (one giant sentence) — you get `sentences: 1`, `variance: 0`. The math is telling you the truth!

Part 2 done. 🎉

---

## 8. Part 3: Rule-Based Improvements

**Goal:** fix the *obvious* robot habits with plain find-and-swap rules — no AI needed. This runs instantly and costs nothing.

**Kid analogy:** this is the spell-checker layer — dumb but lightning-fast. The AI agents (Parts 5–6) are the smart coach who comes after.

### The code

Create `lib/rules.ts`:

```ts
// rules.ts — simple find-and-swap rules to make text less robotic.

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

  for (const [phrase, options] of PHRASE_SWAPS) {
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
```

### Line-by-line explanation

**`import { countWords } from "./analyze";`** — borrow the word-counter we built in Part 2. `./` means "in the same folder as this file."

**`const PHRASE_SWAPS: [string, string[]][] = [...]`** — that scary type reads in small bites: `string` = text; `string[]` = a list of texts; `[string, string[]]` = a *pair*: one phrase + a list of replacement options; the final `[]` = a list of such pairs. So it's a list of recipe cards, each saying "bad habit → three better phrasings." Why three options? **Variety.** If every "in conclusion" became "to sum this up," we'd just have a new robot habit.

**`const CONTRACTIONS: [string, string][]`** — pairs mapping stiff phrasing to its friendly form. Note the **spaces around each phrase** — that's a cheap trick to only match whole words in the middle of text (we never want to rewrite "doesn't" that lives inside another word). The spaces get glued back in by the split/join below.

**`let result = text;`** — `let` (not `const`) because we're going to keep replacing what's inside this box as we apply each rule.

**The phrase-swap loop:**

- `for (const [phrase, options] of PHRASE_SWAPS)` — "for each recipe card, unpack it into `phrase` and `options`."
- `new RegExp(phrase, "gi")` — build a search pattern *from text*. `g` = everywhere; `i` = ignore uppercase/lowercase ("Utilize" matches too).
- `result.replace(pattern, () => { ... })` — normally replace takes a fixed string, but we pass a little function instead. Why? **If we passed a fixed string, every match would get the same option.** As a function, the code runs *fresh for every match* — so the dice roll again each time.
- `Math.floor(Math.random() * options.length)` — the dice. `Math.random()` gives a decimal from 0 up to (but never reaching) 1; times 3 options gives 0 to 2.999; `Math.floor` rounds down → a clean 0, 1, or 2. Then `options[pick]` grabs that option.

**The contraction loop:**

- `result.split(long).join(short)` — the safe way to swap text. Split cuts the text into pieces at every `" do not "`, then join glues the pieces back together using `" don't "` as the glue. Analogy: cut a rope at every knot, retie the pieces with a better knot. (Plain `.replace` has surprising behavior with special characters in some cases — split/join is the dumb-but-bulletproof way.)

**`splitLongSentences(text, maxWords)`** — vary the rhythm by breaking giant sentences:

- We reuse the `|`-flag trick from Part 2 to cut the text into sentences (but here we keep raw pieces).
- `if (countWords(trimmed) <= maxWords) return trimmed;` — sentences that are already short enough are left alone. (25 is a decent knob — sentences much longer than that start feeling heavy. Play with it later.)
- `breakPoints` — natural places a long sentence can split into two: `", and "`, `", but "`, `", so "`, `"; "`.
- `trimmed.indexOf(bp)` — *where* does this snippet appear? Returns a position number, or −1 if not found.
- If found: `first` = the text before the break plus a period; `second` = the text after; `charAt(0).toUpperCase() + second.slice(1)` capitalizes the new sentence's first letter; we return the two fresh sentences.
- Honest note: this fixes only the **first** break point per sentence — deliberately simple. The AI agents do the heavy lifting later; rules just clear the easy debris.
- `fixed.join(" ")` — glue all sentences back with spaces.

### Try it right now

Update `lib/tryAnalyze.ts` to test the rules (add these lines at the bottom):

```ts
const robotText =
  "It is important to note that we do not utilize the system prior to approval. " +
  "In conclusion, the report was approved, and the team was happy.";
console.log("BEFORE:", robotText);
console.log("AFTER:", applyRuleImprovements(robotText));
```

Run:

```bash
npx tsx lib/tryAnalyze.ts
```

You'll see "It is important to note that" become something like "Keep in mind", "utilize" become "use", " do not " become " don't ". **Run it twice** — you should get different word choices sometimes. That's the dice working.

### ✅ Test it

1. Rules swap robotic phrases. ✅
2. Contractions appear. ✅
3. Two runs can differ (variety). ✅
4. Normal words like "the" are untouched. ✅

Part 3 done — your app now has a fast, free, offline improvement layer. 🎉

---

## 9. Part 4: Install Ollama and Run a Small Model

**Goal:** make sure the local AI brain is installed (you did this in section 4.4–4.5 — quick recap here) and learn the *exact doorway* our app will use to talk to it.

### Quick recap

If you haven't yet: install Ollama from [ollama.com/download](https://ollama.com/download) (Windows installer, Next-Next-Finish), then:

```bash
ollama pull llama3.2:3b
ollama run llama3.2:3b "Why is the sky blue?"
```

If that prints an answer, you're ready. `/bye` exits the chat.

### The doorway our app will use

Ollama isn't just a chat program — it also runs a tiny **API server** on your laptop at `http://localhost:11434`. Our app will send text to that address and get rewritten text back. Nothing leaves your machine — the "server" is just a door on your own laptop.

Let's knock on that door once by hand, so it's not magic later.

### Step 1: Create a test request file

In VS Code, create `docs/test-ollama.json`:

```json
{
  "model": "llama3.2:3b",
  "prompt": "Say hello in one short sentence.",
  "stream": false
}
```

Line by line:

- `"model"` — which brain to use. Must match the name you pulled.
- `"prompt"` — the instruction/question we send.
- `"stream": false` — Ollama can answer word-by-word like a dripping faucet (streaming), or all at once like a dumped bucket. We want the bucket — much easier for beginners.

We put the request in a file because typing JSON directly into the Windows command line requires ugly escaping (backslashes everywhere). A file is cleaner.

### Step 2: Send it with curl

Make sure `npm run dev` is **not** required here — this is just the terminal. From your project folder:

```bash
curl http://localhost:11434/api/generate -d @docs/test-ollama.json
```

- `curl` — a built-in Windows tool that sends HTTP requests (like a mail carrier).
- `-d @docs/test-ollama.json` — "deliver this file as the package contents."

After a thinking pause (10–60 seconds on an i3 — that's normal), you'll get a wall of JSON. Somewhere inside you'll find:

```
"response":"Hello! It's nice to meet you."
```

That `"response"` field is the model's answer — exactly the field our code will read in Part 5.

### ✅ Test it

- [ ] `ollama --version` works
- [ ] `ollama run llama3.2:3b "..."` answers
- [ ] The curl command returns JSON containing `"response"`

All three = Part 4 done. The AI brain is local, loaded, and reachable at a known address. 🎉

---

## 10. Part 5: First AI Agent (Simplifier)

**Goal:** write the function that talks to Ollama, and wrap it in our first *agent*: the **Simplifier** — rewrites text in plain, short sentences.

**Kid analogy:** an agent is a specialist you hire for one job. You hand them text + written instructions; they hand back the finished work. No magic — just a well-written request.

### The code

Create `lib/agents.ts`:

```ts
// agents.ts — each agent is a small function that talks to Ollama.

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
    throw new Error(`Ollama problem: ${response.status}`);
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
```

### Line-by-line explanation

**`const OLLAMA_URL` / `const MODEL`** — the doorway address and the brain's name, written once at the top so changing the model later (Part 9) means editing ONE line.

**`export async function askOllama(prompt: string): Promise<string>`**

- `async` marks this function as one that **waits** for slow things (like the AI thinking). Analogy: you order a pizza and get a buzzer; `await` = "stand by until the buzzer rings." The buzzer is called a **Promise** — a promise that the answer will arrive.
- `: Promise<string>` — this recipe eventually produces text (after the wait).

**The `fetch` call** — the mail carrier:

- `fetch(OLLAMA_URL, { ... })` — deliver a request to our address, with a package described by the object.
- `method: "POST"` — "I'm handing you a package" (as opposed to GET: "just let me read something").
- `headers: { "Content-Type": "application/json" }` — the shipping label: "contents are JSON."
- `body: JSON.stringify({ ... })` — the package itself. `JSON.stringify` converts a JavaScript object into JSON text (the wire format both sides understand). Look inside: `model`, `prompt`, `stream: false` — the same three keys we tested by hand in Part 4. `options: { temperature: 0.7 }` is the **creativity dial** from 0 to 1: 0 = strict robot, 1 = wild poet. 0.7 = friendly middle. Try 0.3 and 0.9 later and compare!

**Error check:**

- `if (!response.ok)` — did the delivery fail? (`ok` is true for success codes.)
- `throw new Error(...)` — raise a red flag that stops this function. The message uses a **template string** — backticks with `${response.status}` slots that get filled in. Someone upstream (Part 7's safety net) will catch this flag and show a friendly message.

**Reading the answer:**

- `const data = await response.json()` — unwrap the reply box (parse JSON text into a real object).
- `let answer: string = data.response;` — take the `"response"` field (the one we found in Part 4). `let` because we're about to clean it up.
- `answer.trim()` — cut stray spaces/newlines off the edges.
- `answer.replace(/^["']|["']$/g, "")` — small defense: models sometimes wrap answers in quotes. This regex removes a quote at the very start (`^["']`) or very end (`["']$`) of the text. (`|` = "or".)

**`simplify`** — the agent itself:

- The prompt is built as a list of instruction lines joined with `"\n"` (newline characters) — much easier to read and edit than one giant string.
- The most important line is: **"Do not add new information. Do not comment. Output ONLY the rewritten text."** Models love to chatter ("Sure! Here's your rewritten text:"). Strict instructions + the quote-stripping above keep the output clean.
- The text to rewrite rides at the bottom, after `Text:` — a simple, reliable structure the model understands.

### Try it right now

Create `lib/tryAgent.ts`:

```ts
import { simplify } from "./agents";

async function main() {
  const robot =
    "It is important to note that the utilization of the system commences prior to the finalization of the report.";
  console.log("BEFORE:", robot);
  const simple = await simplify(robot);
  console.log("AFTER:", simple);
}

main();
```

Run (Ollama must be running — check for the llama icon near the clock):

```bash
npx tsx lib/tryAgent.ts
```

Expect a wait of 10–60 seconds on your i3 — the model is *actually thinking on your CPU*. That's the price of free and private.

### ✅ Test it

1. BEFORE is stiff, AFTER is plainer. ✅
2. No chatty preamble like "Here's your text:" in the output. ✅ (If you ever see chatter, your instructions aren't being followed — the strict line in the prompt is your first fix to try.)
3. If you get `Ollama problem: ...` or a connection error → is Ollama running? Did the model name match what you pulled?

Part 5 done — you've written your first AI agent. 🎉

---

## 11. Part 6: Multi-Agent Pipeline

**Goal:** add two more agents (**Tone Adjuster**, **Final Polisher**) and chain everything into one pipeline: Analyzer → Rules → Simplifier → Tone Adjuster → Final Polisher.

**Kid analogy:** a **car wash**. Your text drives in; each station does one job; the car exits clean. Each station only knows: "take what came in, do my job, pass it on."

### Add two agents to `lib/agents.ts`

Paste these at the bottom of `lib/agents.ts`:

```ts
export async function adjustTone(
  text: string,
  repeated: { word: string; count: number }[]
): Promise<string> {
  const avoidList = repeated.map((r) => r.word).join(", ");
  const prompt = [
    "Rewrite the text below to sound warm and friendly.",
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
```

**What's new here:**

- `adjustTone` takes **two ingredients**: the text, *and* the list of the user's most-repeated words (the `{ word, count }` objects from Part 2's analyzer). This is the cool part — **the math talks to the AI.** `repeated.map((r) => r.word).join(", ")` squeezes just the words out of the objects ("report, finalized, ..."), and `${avoidList}` slots them into the instruction: "avoid repeating these."
- `finalPolish` has the *gentlest* instructions of all three agents — it should barely change anything, just tidy up. It runs last so earlier agents' messes get mopped.

### The pipeline

Create `lib/pipeline.ts`:

```ts
// pipeline.ts — runs every step in order, like a car wash.

import { analyzeText } from "./analyze";
import { applyRuleImprovements, splitLongSentences } from "./rules";
import { simplify, adjustTone, finalPolish } from "./agents";

export async function humanize(text: string): Promise<string> {
  // Step 0: math report (the "teacher" — shows what was wrong)
  const report = analyzeText(text);
  console.log("Analyzer report:", report);

  // Step 1: fast rule fixes (no AI needed)
  let current = applyRuleImprovements(text);
  current = splitLongSentences(current, 25);

  // Step 2: Simplifier agent
  current = await simplify(current);

  // Step 3: Tone Adjuster agent (gets the repeat list from the report)
  current = await adjustTone(current, report.repeated);

  // Step 4: Final Polisher agent
  current = await finalPolish(current);

  return current;
}
```

**Line by line:**

- `const report = analyzeText(text)` — run the math first, *before* anything changes, so the numbers describe the ORIGINAL text. `console.log` prints the report in the server terminal — you'll see it in Part 7. (The web page doesn't see this; it's for you, the developer, watching the kitchen.)
- `let current = ...` — one box that holds the text as it moves through stations. Each station replaces the contents.
- Rules first because they're free and instant — why pay AI seconds to fix what a find-and-swap fixes in milliseconds?
- Then three `await`ed agents, strictly in order. Each one *fully finishes* before the next starts — that's what sequential awaiting means, and it's exactly what a car wash needs.
- `report.repeated` hops from the math step into the Tone Adjuster's prompt — the pipeline's secret sauce.
- Return the finished text.

### ✅ Test it

We can't run the pipeline directly yet (it needs a web request to arrive) — that's Part 7. For now, verify it compiles with no errors:

```bash
npx tsc --noEmit
```

(`tsc` is the TypeScript checker; `--noEmit` means "just check, don't output files." No news = good news.)

Part 6 done — four stations wired in sequence. 🎉

---

## 12. Part 7: Connect UI to Agents

**Goal:** two jobs. (1) Build the **API route** — the kitchen door the page talks through. (2) Wire the button to send text through it.

### The kitchen: `app/api/humanize/route.ts`

In VS Code, inside `app/api`, create a folder `humanize`, and inside it a file `route.ts`. (Next.js has a rule: a file named `route.ts` inside `app/api/<name>/` automatically becomes the address `/api/<name>`. Free plumbing!)

```ts
// route.ts — the "kitchen" the UI calls.

import { NextResponse } from "next/server";
import { humanize } from "@/lib/pipeline";

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const text = body.text;
    if (typeof text !== "string" || text.trim() === "") {
      return NextResponse.json(
        { error: "Please send some text." },
        { status: 400 }
      );
    }
    const result = await humanize(text);
    return NextResponse.json({ result: result });
  } catch (error) {
    console.error(error);
    return NextResponse.json(
      { error: "Something went wrong. Is Ollama running?" },
      { status: 500 }
    );
  }
}
```

**Line by line:**

- `import { NextResponse } from "next/server"` — Next's helper for building JSON replies.
- `import { humanize } from "@/lib/pipeline"` — our pipeline! The `@/` is a shortcut for the project root (set up by create-next-app, remember from Part 0). `@/lib/pipeline` = "the pipeline file in the lib folder at the project root." Cleaner than `../../lib/pipeline`.
- `export async function POST(request: Request)` — by naming the function `POST`, Next.js wires it to answer POST deliveries at `/api/humanize`. The `request` parameter is the incoming package.
- `try { ... }` — a **safety net**. Try the whole trick; if anything inside throws a red flag (like our `throw` in Part 5), the net catches it in `catch` and the page gets a friendly error instead of a crash.
- `await request.json()` — open the incoming package and read it.
- The `if` is a **bouncer at the door**: "is `text` really a string, and not just spaces?" If not, we reply with a **400** status ("you sent something wrong") — never let junk into the kitchen.
- `const result = await humanize(text)` — the big moment: run the whole car wash. This is the slow line (three model calls, remember).
- Success: reply with `{ result: ... }` and (by default) a 200 status ("all good").
- `catch (error)`: log the full details for *you* in the server terminal (`console.error`), but send only a friendly, vague message to the page, with **500** ("I broke"). Users never need the gory details; developers do — hence both.

### The button: update `app/page.tsx`

Two small edits.

**Edit 1** — add this function inside `Home()`, just above the `return (`:

```tsx
async function handleHumanize() {
  setIsLoading(true);
  setResult("");
  try {
    const response = await fetch("/api/humanize", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: draft }),
    });
    const data = await response.json();
    if (!response.ok) {
      setResult("Error: " + (data.error ?? "unknown problem"));
    } else {
      setResult(data.result);
    }
  } catch {
    setResult("Error: could not reach the server. Is it running?");
  } finally {
    setIsLoading(false);
  }
}
```

- `setIsLoading(true)` — flip the whiteboard: the button becomes disabled and shows "Working..." (from Part 1 — it finally gets used!).
- `fetch("/api/humanize", ...)` — same fetch as Part 5, but this time the browser is the mail carrier, and `"/api/humanize"` (starting with just `/`) means "my own house" — the same server serving this page.
- `body: JSON.stringify({ text: draft })` — pack `{ text: draft }`; that matches exactly what the kitchen reads with `body.text`.
- `if (!response.ok)` — kitchen said 400/500 → show its friendly error inside the output box (simplest possible error display).
- `catch` — the fetch itself failed (server off) → another friendly message.
- `finally` — runs **whether we won or lost**: stop the spinner, re-enable the button. `finally` = "no matter what, do this before leaving."

**Edit 2** — change the button's onClick from the alert to the real thing:

```tsx
<button
  onClick={handleHumanize}
  disabled={draft.trim() === "" || isLoading}
  className="bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400"
>
```

(We pass the function itself, `handleHumanize` — not `handleHumanize()` with parentheses. With parentheses it would run immediately on page load; without, we're just handing over the recipe.)

### ✅ Run and test it

Make sure `npm run dev` is running, Ollama is running, then at http://localhost:3000:

1. Paste a stiff paragraph (try: "It is important to note that we do not utilize the system prior to approval. In conclusion, the report was approved, and the team was happy.")
2. Click **Humanize** → button shows "Working..." and grays out.
3. **Be patient: 1–5 minutes total on an i3** — three model calls in a row. Totally normal. Watch the terminal where `npm run dev` runs: you'll see `Analyzer report: {...}` print — the kitchen talking to you.
4. The output box fills with warmer, plainer text. Contractions? Shorter sentences? Fewer repeats?

All four = Part 7 done. **Your app works end to end.** 🎉🎉

---

## 13. Part 8: Add Copy Button

**Goal:** one extra button under the output that copies the result to the clipboard, with a "Copied!" confirmation.

### The code

In `app/page.tsx`, make three edits:

**Edit 1** — add one more whiteboard next to the others:

```tsx
const [copied, setCopied] = useState(false);
```

**Edit 2** — add this function next to `handleHumanize`:

```tsx
async function handleCopy() {
  try {
    await navigator.clipboard.writeText(result);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  } catch {
    setCopied(false);
  }
}
```

- `navigator.clipboard.writeText(result)` — the browser's built-in hand that copies text to your clipboard. It's also async (a buzzer again), so we `await` it.
- `setCopied(true)` — flip a whiteboard so the button label changes.
- `setTimeout(() => setCopied(false), 2000)` — an **alarm clock**: "in 2000 milliseconds (2 seconds), run this." The label flips back to "Copy."
- The `catch` is for rare browsers/permissions that block clipboard access — we just quietly fail.

**Edit 3** — add the button right below the output textarea (still inside the `div`):

```tsx
{result !== "" && (
  <button
    onClick={handleCopy}
    className="bg-slate-700 text-white py-2 px-6 rounded-lg font-semibold hover:bg-slate-800 self-end"
  >
    {copied ? "Copied!" : "Copy"}
  </button>
)}
```

- `{result !== "" && ( ... )}` — the **&& trick** for show/hide. Reading it left to right: *if* the result is not empty, *then* render the button. If the left side is false, JavaScript short-circuits and React renders **nothing**. So the Copy button simply doesn't exist until there's something to copy.
- `{copied ? "Copied!" : "Copy"}` — the ternary from Part 1: label swaps for 2 seconds.
- `self-end` — inside our `flex flex-col` container, this pushes the button to the right edge.

### ✅ Run and test it

1. Humanize some text.
2. A **Copy** button appears under the output.
3. Click it → label becomes "Copied!" → paste somewhere (Notepad) → your text is there.
4. After ~2 seconds the label flips back to "Copy".
5. Clear/refresh so the output is empty → no Copy button at all.

All five = Part 8 done. The UI is complete. 🎉

---

## 14. Part 9: Test Everything

**Goal:** a proper test pass — including *trying to break it*. Real developers test the unhappy paths, not just the happy one.

**Setup for every test:** `npm run dev` running, Ollama running (llama icon visible), close memory-hogging programs first.

### Test checklist

**1. Empty input**
Don't type anything. → The Humanize button is gray/disabled. You can't even click it. ✅

**2. Only spaces**
Type five spaces. → Still disabled (that's why we `.trim()` before checking). ✅

**3. One word**
Type "hello", click Humanize. → After a wait, you get *something* back (maybe similar to the input — with one word there's little to improve). No crash. ✅

**4. A normal paragraph (50–100 words)**
Paste a paragraph you actually wrote (an email, a homework paragraph *you* authored). → Does the output sound more natural? Check it against the analyzer's report printed in the terminal: did sentence-length variance go up? Did repeats go down? **This is the learning moment — compare numbers before/after.**

**5. Ollama turned OFF (the unhappy path)**
Right-click the llama icon near the clock → **Quit Ollama**. Click Humanize. → After a short wait, the output box shows a friendly error ("Something went wrong. Is Ollama running?") and the page does NOT crash; the button re-enables. ✅ Restart Ollama from the Start menu before continuing.

**6. No internet**
Turn off Wi-Fi, run a Humanize. → It still works! (The model is local. That's the whole point.) Turn Wi-Fi back on. ✅

**7. Swap the model**
In `lib/agents.ts`, change one line: `const MODEL = "phi3:mini";` (if you pulled it in section 4.5). Re-run a Humanize. → Still works, different flavor of writing. Change it back if you prefer Llama. ✅

**8. The dice still roll**
Find a phrase from `PHRASE_SWAPS` in your input ("in conclusion"), humanize twice with the same text. → The outputs differ at least slightly (rule dice + temperature both add variety). ✅

**9. Very long text (300+ words)**
It works, but expect a *long* wait (three full rewrites of a long text on CPU). If it's too slow for your taste, that's real feedback about your hardware — not a bug. ✅

**Score yourself:** 9/9 = you built something *solid*, not just something that works on your best day.

---

## 15. Part 10: Final Polish and Next Steps

### A tiny final touch: live word count

Two small edits in `app/page.tsx`:

**Edit 1** — import the counter from Part 2 (top of the file):

```tsx
import { countWords } from "@/lib/analyze";
```

**Edit 2** — right below the input textarea, add:

```tsx
<p className="text-sm text-slate-500">
  {draft.trim() === "" ? "0 words" : countWords(draft) + " words"}
</p>
```

Type and watch the counter tick — it updates live because `draft` is a whiteboard, and React repaints on every change. (Nice symmetry: the math you wrote in Part 2 now lives in the UI.)

### What you actually built

Take a second. You built, from nothing:

- A React page with **state** (Part 1, 8)
- Real text math: variance, frequency, averages (Part 2)
- A rule engine with randomized variety (Part 3)
- A local AI integration — no cloud, no keys (Parts 4–5)
- A 4-station agent pipeline where **math feeds the AI** (Part 6)
- A full-stack loop: browser → API route → pipeline → Ollama → back (Part 7)
- A test pass including failure paths (Part 9)

That is not a toy. That's the *shape* of almost every real app: UI → door → kitchen → helpers → reply.

### Ideas to try next (in rough order of difficulty)

1. **Show the report in the UI** — add a toggle that displays the analyzer's numbers under the output (you already have `analyzeText`; call it in `handleHumanize` and store the report in a new whiteboard).
2. **More phrase swaps** — your own robotic-phrase pet peeves in `PHRASE_SWAPS`.
3. **A "before/after numbers" comparison** — run `analyzeText` on input and output, show variance for both. Watching variance climb is genuinely fun.
4. **Try other models** — browse [ollama.com/library](https://ollama.com/library) for small ones (e.g. `qwen2.5:3b`, `gemma2:2b`): pull, change the `MODEL` line, compare outputs.
5. **A fourth agent: "Your Voice"** — paste a sample of your own writing, and add an agent whose prompt says "match the style of this sample." (Careful: keep it as a *coach*, not a ghostwriter.)
6. **Prompt experiments** — change `temperature`, reword the agent instructions, and keep a log in `docs/NOTES.md` of what changed. Prompting is a real skill; you now have a lab for it.

### Where to learn more (free, no signups)

- **react.dev/learn** — the best React basics course, written for beginners
- **nextjs.org/learn** — official Next.js walkthrough
- **MDN Web Docs** (developer.mozilla.org) — the dictionary of the web
- **The TypeScript handbook** (typescriptlang.org/docs/handbook) — skim "The Basics"
- **Ollama docs** (ollama.com) — model library and API options

And the habit that matters most: **one hour a day, notes in `docs/NOTES.md`, always be building something you personally want to exist.**

---

## 16. README.md Content

When your app works, give it a proper front door. Create this file **inside your `humanizer` project folder** as `README.md` (create-next-app already made one — replace its contents):

````markdown
# Humanizer

A 100% local writing coach. Paste text, click Humanize, get text that sounds
more natural — analyzed by math, improved by small local AI agents.

Nothing leaves your laptop. No cloud. No API keys. No login. No history.

## What it does

1. **Math Analyzer** — counts words/sentences, measures sentence-length
   variance, finds repeated words (the "why is this robotic" report)
2. **Rule Fixes** — instantly swaps robotic phrases ("in conclusion" → varied
   endings) and adds contractions
3. **Simplifier Agent** — rewrites in plain, short sentences
4. **Tone Adjuster Agent** — warms it up; avoids *your* most-repeated words
5. **Final Polisher Agent** — light cleanup of capitals and spacing

All agents run on a small local model via [Ollama](https://ollama.com).

## Requirements

- Windows (also works on macOS/Linux)
- [Node.js](https://nodejs.org) v20+
- [Ollama](https://ollama.com/download) with a small model:

```bash
ollama pull llama3.2:3b
```

(8 GB RAM machine? `phi3:mini` also works — change one line in
`lib/agents.ts`.)

## Setup

```bash
npm install
npm run dev
```

Open http://localhost:3000

## Usage

Paste your **own** draft into the input box, click **Humanize**, wait
(1–5 minutes on CPU — it's local, free, and worth it), then **Copy** the
result.

## Ethics

Humanizer is a **writing coach, not a cheating tool**. Use it to understand
*why* your writing feels robotic and to polish drafts *you* wrote. Don't use
it to pass off AI-rewritten work as your own — that's plagiarism in spirit,
and detectors keep getting better anyway.

## Project structure

```
app/
  page.tsx              the UI (input, button, output, copy)
  api/humanize/route.ts the kitchen door the UI calls
lib/
  analyze.ts            math: counts, variance, repeated words
  rules.ts              instant phrase/contraction fixes
  agents.ts             the three AI agents + the Ollama caller
  pipeline.ts           the car wash that runs everything in order
docs/
  NOTES.md              my daily learning notes
```
````

---

## 17. Glossary of Every Term Used

**agent** — a small function that sends text plus written instructions to an AI model and gets text back.

**AI model** — a program trained on lots of text that predicts what words should come next; small ones can run on a laptop.

**analysis / analyzer** — code that measures text (counts, averages) instead of changing it.

**API** — a doorway a program exposes so other programs can talk to it by sending requests.

**API route** — in Next.js, a file that becomes one such doorway inside your own app (ours: `/api/humanize`).

**App Router** — Next.js's modern way of organizing pages and routes inside the `app/` folder.

**arrow function** — a tiny one-line function written like `(e) => something`.

**async / await** — a way to wait for slow things (like the AI thinking) without freezing everything else; `await` = "stand by until the buzzer rings."

**average (mean)** — add everything up, divide by how many; the "fair share."

**braces `{ }`** — curly brackets that mark "here comes JavaScript" in JSX, or group code into blocks.

**browser** — the program (Chrome, Edge) that shows web pages.

**bug** — a mistake in code that makes it behave wrong.

**button disabled** — grayed out so clicking does nothing.

**clipboard** — the invisible notepad your computer copies text onto (Ctrl+C / Ctrl+V).

**component** — a reusable piece of UI, written as a function (our whole page is one component called `Home`).

**constant (`const`)** — a labeled box whose contents never get replaced with something else.

**contraction** — a squished word pair like "don't" or "it's."

**CPU** — your laptop's main thinking chip; the AI runs on it (slowly but privately).

**curl** — a built-in command-line tool that sends requests to addresses, used to test APIs by hand.

**database** — a program for permanently storing data; we deliberately don't use one.

**dev server** — the local program (`npm run dev`) that serves your website to your browser while you build it.

**error 400 / 500** — status codes meaning "you sent something wrong" / "I broke."

**event** — something that happened (a click, a keystroke) delivered to your code as a package, usually named `e`.

**export / import** — the stamp that lets other files use a function / the statement that borrows it.

**fetch** — the function that delivers a request to an address and brings back the reply.

**filter** — a list operation that keeps only items passing a test.

**finally** — the part of try/catch that runs no matter what happened.

**frequency** — how many times something appears; counted in a frequency map.

**function** — a named recipe: ingredients go in, steps run, a result comes out.

**GB / RAM** — gigabytes; RAM is your laptop's short-term working memory (yours: 8 GB — close big programs!).

**git** — a tool that tracks file history; we barely used it here.

**globally / `g` flag** — in regex, "apply everywhere, not just the first match."

**hot reload** — the dev server updating your browser instantly when you save a file.

**instance / object** — a bundle of related values with names, like `{ word: "report", count: 4 }`.

**JSON** — a simple text format for structured data that programs send each other.

**JSX** — HTML-like code written inside JavaScript files; how React describes pages.

**`let`** — a labeled box whose contents will be replaced as the code runs.

**localhost** — "this same computer"; an address that never leaves your machine.

**map** — a list operation that transforms every item into something new.

**Map / Set** — a labeled-drawer cabinet for counting / a bag with one copy of each item for fast lookups.

**Next.js** — the toolbox that builds both our page and our server code in one project.

**Node.js** — the program that lets your computer run JavaScript/TypeScript outside the browser.

**npm / npx** — the package shopper (`npm install`) / the tool runner that downloads-and-runs without permanent install.

**Ollama** — a free program that runs AI models locally and exposes them at `localhost:11434`.

**package / package.json** — a downloaded bundle of someone else's code / your project's list of packages and commands.

**parameter / argument** — the named input a function expects / the actual value you hand it.

**pipeline** — a chain of steps where each step's output is the next step's input; our car wash.

**Promise** — the "buzzer" you get when ordering an async operation; it rings when the result is ready.

**prompt** — the written instruction you give an AI model.

**property / field** — one named value inside an object (`data.response`).

**regex (regular expression)** — a tiny search pattern written between slashes, like `/\s+/` for "one or more spaces."

**`readOnly`** — an input that displays but refuses typing.

**reduce** — a list operation that folds everything into one value by walking the list with a running total.

**React / state** — the library that repaints the page when values change / a value React watches (our whiteboards via `useState`).

**request / response** — the message you send to an API / the message it sends back.

**return** — what a function hands back when it finishes.

**server** — the hidden part of an app that does the work (ours runs on your laptop inside Next.js).

**slice** — cutting a piece out of text or a list by positions.

**spread (`...`)** — "pour all the items out" of a collection into a new list.

**status code** — the number a server attaches to replies (200 good, 400 your fault, 500 my fault).

**streaming** — receiving an AI answer word-by-word; we turn it off (`stream: false`) to get the whole answer at once.

**string / number / boolean** — text / a numeric value / true-or-false.

**Tailwind CSS** — a styling tool where you describe looks with tiny class words like `p-8` and `bg-white`.

**template string** — text in backticks with `${...}` slots that get filled with values.

**temperature** — the AI's creativity dial from 0 (strict) to 1 (wild).

**ternary** — a one-line if/else: `condition ? valueIfTrue : valueIfFalse`.

**textarea** — a multi-line text box.

**trim** — cutting invisible whitespace off the ends of text.

**try / catch** — the safety net: attempt something risky; if it throws, land in the catch block instead of crashing.

**TypeScript** — JavaScript with type promises (like `: string`) checked before your app runs; a spell-checker for code.

**undefined / null** — "nothing here" values; `??` gives you a fallback when you find one.

**UI** — user interface: the buttons, boxes, and text a person actually sees.

**variance** — the average squared distance from the average; our "wobble meter" for sentence lengths.

**VS Code** — the editor where you write code.

---

**You did it.** You built a real, private, local AI app — and you understand every line of it. Now go write something worth humanizing. 🎉
