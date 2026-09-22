"use client";

import { useState } from "react";
import Image from "next/image";


export default function Home() {
  const [draft, setDraft] = useState("");
  const [result, setResult] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  return (
    <main className="min-h-screen bg-slate-100 p-8">
      <h1 className="text-3xl font-bold text-center mb-2">Humanizer</h1>
      <p className="text-center text-slate-500 mb-8">
        Runs Locally, No money needed.
      </p>

      <div className="max-w-3xl mx-auto flex flex-col gap4">
        <textarea
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          placeholder="Paste Your Text Here..."
          className="w-full h-48 p-4 rounded-lg border border-slate-300 bg-white"
        />

        <button
          onClick={() => alert("Button works!")}
          disabled = {draft.trim() === "" || isLoading}
          className="bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-slate-400">
            {isLoading ? "working...":"Humanize"}
          </button>

        <textarea
          value={result}
          readOnly
          placeholder="The Humaized Text Will Appear Here..."
          className="w-full h-48 p-4 rounded-lg border border-slate-300 bg-white"/>
      </div>
    </main>
  );
}

