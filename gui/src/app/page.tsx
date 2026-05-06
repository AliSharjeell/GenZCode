"use client";

import { useEffect, useState } from "react";
import Editor, { Monaco } from "@monaco-editor/react";
import { setupGenZLanguage } from "@/lib/genzLanguage";
import { Button } from "@/components/ui/button";

const defaultCode = `// Variables
lowkey x: num = 42;
lowkey name: txt = "bruh";

// Conditional
sus (x > 10) {
    spill_tea("x is big");
} deadass {
    spill_tea("x is small");
}

// Function
vibe_check greet() {
    spill_tea(name);
    slay 0;
}`;

export default function Home() {
  const [code, setCode] = useState(defaultCode);

  const handleEditorWillMount = (monaco: Monaco) => {
    setupGenZLanguage(monaco);
  };

  const handleEditorChange = (value: string | undefined) => {
    if (value) setCode(value);
  };

  const handleRun = () => {
    console.log("Running code...", code);
    // In a real app, this would send code to the backend compiler.
  };

  return (
    <div className="flex flex-col h-screen bg-zinc-950 text-zinc-50 font-sans selection:bg-zinc-800">
      {/* Header */}
      <header className="flex items-center justify-between px-6 py-4 border-b border-zinc-900 bg-zinc-950">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded bg-zinc-100 text-zinc-950 flex items-center justify-center font-bold text-xl leading-none">
            G
          </div>
          <h1 className="text-xl font-semibold tracking-tight text-zinc-100">GenZCode Studio</h1>
        </div>
        <div className="flex items-center gap-4">
          <span className="text-sm text-zinc-400 font-mono bg-zinc-900 px-3 py-1 rounded-md">main.genz</span>
          <Button 
            onClick={handleRun}
            className="bg-zinc-100 text-zinc-900 hover:bg-zinc-200 transition-colors font-medium px-6 rounded-md shadow-sm"
          >
            Run
          </Button>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 flex flex-col p-6 overflow-hidden bg-zinc-950">
        <div className="flex-1 rounded-xl overflow-hidden border border-zinc-800 bg-[#09090b] shadow-2xl relative ring-1 ring-white/5">
          <Editor
            height="100%"
            defaultLanguage="genz"
            theme="genzDark"
            value={code}
            onChange={handleEditorChange}
            beforeMount={handleEditorWillMount}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: "var(--font-geist-mono), ui-monospace, SFMono-Regular, monospace",
              lineHeight: 1.6,
              padding: { top: 24, bottom: 24 },
              scrollBeyondLastLine: false,
              smoothScrolling: true,
              cursorBlinking: "smooth",
              cursorSmoothCaretAnimation: "on",
              formatOnPaste: true,
              renderLineHighlight: "all",
            }}
          />
        </div>
      </main>
    </div>
  );
}
