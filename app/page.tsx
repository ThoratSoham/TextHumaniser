"use client";

import { useState } from "react";
import Image from "next/image";


export default function Home() {
  const [draft, setDraft] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  async function handleHumanize() {
    setIsLoading(true);
    setResult("");
    try {
      const response = await fetch("/api/humanize", {
        method: "POST",
        headers: { "Content-type": "application/json"},
        body: JSON.stringify({ text: draft}),
      });
      const data = await response.json();
      if (!response.ok) {
        setResult("Error: " + (data.error ?? "unknown problem"));
      } else {
        setResult(data.result);
      }
    } catch {
      setResult("Error: could not reach the server. Is it Running?");
    } finally {
      setIsLoading(false);
    }
  }

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      setCopied(false);
    }
  }

  return (
    <main className="min-h-screen bg-neutral-950 text-neutral-200 p-6 sm:p-12 selection:bg-purple-900 selection:text-purple-200">
  {/* Header Section */}
  <div className="max-w-3xl mx-auto text-center mb-10 space-y-2">
    <h1 className="text-4xl sm:text-5xl font-serif font-black tracking-widest uppercase text-transparent bg-clip-text bg-gradient-to-b from-purple-300 via-purple-500 to-purple-900 drop-shadow-[0_2px_10px_rgba(168,85,247,0.2)]">
      Humanizer
    </h1>
    <p className="text-sm font-mono tracking-widest text-purple-400/60 uppercase">
      ⚡ Runs Locally — Bound by No Toll
    </p>
  </div>

  {/* Main Container */}
  <div className="max-w-3xl mx-auto flex flex-col gap-6">
    
    {/* Input Textarea */}
    <div className="relative group">
      <textarea
        value={draft}
        onChange={(e) => setDraft(e.target.value)}
        placeholder="Inscribe your draft into the shadows..."
        className="w-full h-52 p-5 rounded-xl border border-purple-950/80 bg-neutral-900/90 text-purple-100 placeholder-neutral-600 focus:outline-none focus:border-purple-600 focus:ring-1 focus:ring-purple-600/50 transition-all duration-300 resize-none font-sans text-sm leading-relaxed shadow-inner shadow-black scrollbar-thin scrollbar-thumb-purple-950"
      />
      <span className="absolute bottom-3 right-4 text-[10px] font-mono tracking-wider text-purple-950 group-focus-within:text-purple-700/60 transition-colors">
        INPUT DRAFT
      </span>
    </div>

    {/* Humanize Action Button */}
    <button
      onClick={handleHumanize}
      disabled={draft.trim() === "" || isLoading}
      className="w-full py-3.5 px-6 rounded-xl font-mono text-xs tracking-[0.25em] uppercase font-bold text-purple-200 bg-gradient-to-r from-purple-950 via-neutral-900 to-purple-950 border border-purple-800/40 hover:border-purple-500 hover:text-white hover:shadow-[0_0_20px_rgba(147,51,234,0.3)] active:scale-[0.99] transition-all duration-300 disabled:opacity-40 disabled:hover:border-purple-800/40 disabled:hover:shadow-none disabled:cursor-not-allowed disabled:active:scale-100 relative overflow-hidden"
    >
      {isLoading ? (
        <span className="animate-pulse text-purple-400">Transmuting...</span>
      ) : (
        "Humanize Text"
      )}
    </button>

    {/* Output Textarea */}
    <div className="relative group">
      <textarea
        value={result}
        readOnly
        placeholder="The transmuted script will emerge here..."
        className="w-full h-52 p-5 rounded-xl border border-purple-950/60 bg-neutral-900/40 text-purple-200/90 placeholder-neutral-700 focus:outline-none resize-none font-sans text-sm leading-relaxed shadow-inner shadow-black cursor-default selection:bg-purple-800 scrollbar-thin scrollbar-thumb-purple-950"
      />
      <span className="absolute bottom-3 right-4 text-[10px] font-mono tracking-wider text-purple-950">
        TRANSMUTED OUTPUT
      </span>
    </div>

    {/* Copy Button */}
    <div className="flex justify-end">
      <button
        onClick={handleCopy}
        disabled={!result}
        className="px-6 py-2.5 rounded-lg text-xs font-mono tracking-widest uppercase border border-purple-900/60 text-purple-300 hover:text-purple-100 hover:bg-purple-950/50 hover:border-purple-600 active:scale-[0.97] transition-all duration-200 disabled:opacity-30 disabled:border-purple-950 disabled:hover:bg-transparent disabled:cursor-not-allowed"
      >
        {copied ? "✦ Extracted to Clipboard ✦" : "Copy Result"}
      </button>
    </div>

  </div>
</main>
  );
}

