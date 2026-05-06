"use client";

import { useState } from "react";
import Editor, { Monaco } from "@monaco-editor/react";
import DocsViewer from "@/components/DocsViewer";
import { setupGenZLanguage } from "@/lib/genzLanguage";
import { Button } from "@/components/ui/button";
import { FileCode2, Plus, Terminal, Play, Trash2, Edit2, Book, FilePlus } from "lucide-react";

type FileData = {
  id: string;
  name: string;
  content: string;
};

const initialFiles: FileData[] = [
  {
    id: "1",
    name: "hello.genz",
    content: `// The classic hello world
spill_tea("hello world");
`
  },
  {
    id: "2",
    name: "math.genz",
    content: `// Variables and math
lowkey x: num = 10;
lowkey y: num = 5;
lowkey result: num = x + y;

spill_tea("Result is:", result);
`
  },
  {
    id: "3",
    name: "brainrot.genz",
    content: `// Extreme brainrot example
lowkey tung_tung_tung_sahur: num = 1;
lowkey skibidi_toilet: txt = "ohio";
lowkey grimace_shake: num = 0;
lowkey ballerina_cappuccina: num = 1;

lowkey aura: num = 100;

sus (aura > 50) {
    spill_tea("W rizz");
    tung_tung_tung_sahur;
} deadass {
    skibidi_toilet;
    grimace_shake;
}

ballerina_cappuccina;
`
  },
  {
    id: "4",
    name: "fizzbuzz.genz",
    content: `// Classic FizzBuzz in GenZCode
lowkey i: num = 1;
lowkey max: num = 20;

spill_tea("Starting FizzBuzz up to", max);

keep_yapping (i <= max) {
    sus (i % 15 == 0) {
        spill_tea("FizzBuzz");
    } deadass sus (i % 3 == 0) {
        spill_tea("Fizz");
    } deadass sus (i % 5 == 0) {
        spill_tea("Buzz");
    } deadass {
        spill_tea(i);
    }
    i = i + 1;
}
`
  },
  {
    id: "5",
    name: "functions.genz",
    content: `// Functions (vibe_checks) in GenZCode
vibe_check calculate_rizz(score: num, bonus: num) {
    lowkey total: num = score + bonus;
    
    sus (total > 100) {
        spill_tea("Unattainable rizz levels detected.");
        slay total;
    } deadass {
        spill_tea("Average rizz.");
        slay total;
    }
}

lowkey my_rizz: num = calculate_rizz(80, 30);
spill_tea("Final rizz score:", my_rizz);
`
  },
  {
    id: "6",
    name: "loops.genz",
    content: `// Demonstrating the keep_yapping loop
lowkey count: num = 0;

spill_tea("Starting the count...");

keep_yapping (count < 10) {
    count = count + 1;
    
    sus (count == 5) {
        spill_tea("Halfway there! Skipping 5...");
        next_up;
    }
    
    spill_tea("Current count is:", count);
}

spill_tea("Done yapping!");
`
  },
  {
    id: "7",
    name: "switch.genz",
    content: `// Using ratio and bet (switch/case)
lowkey grade: txt = "B";

ratio (grade) {
    bet "A": {
        spill_tea("W grade, no cap");
        bounce;
    }
    bet "B": {
        spill_tea("Not bad, valid");
        bounce;
    }
    bet "C": {
        spill_tea("Bro fell off");
        bounce;
    }
    nvm: {
        spill_tea("L + ratio + failed");
        bounce;
    }
}
`
  },
  {
    id: "8",
    name: "arrays.genz",
    content: `// Array basics in GenZCode
lowkey scores: num[] = [100, 95, 80, 42];

spill_tea("First score:", scores[0]);

// Modify an element
scores[3] = 69;
spill_tea("Modified last score:", scores[3]);

// Loop over array (using index)
lowkey i: num = 0;
keep_yapping (i < 4) {
    spill_tea("Score at index", i, "is", scores[i]);
    i = i + 1;
}
`
  },
  {
    id: "9",
    name: "factorial.genz",
    content: `// Calculating Factorial using recursion
vibe_check factorial(n: num) {
    sus (n == 0) {
        slay 1;
    } deadass {
        slay n * factorial(n - 1);
    }
}

lowkey num_to_check: num = 5;
lowkey result: num = factorial(num_to_check);

spill_tea("The factorial of", num_to_check, "is", result);
`
  },
  {
    id: "10",
    name: "fibonacci.genz",
    content: `// Generating the Fibonacci sequence
vibe_check fib(n: num) {
    sus (n <= 1) {
        slay n;
    }
    slay fib(n - 1) + fib(n - 2);
}

lowkey terms: num = 10;
lowkey i: num = 0;

spill_tea("Fibonacci Sequence up to", terms, "terms:");

keep_yapping (i < terms) {
    spill_tea("Term", i, "->", fib(i));
    i = i + 1;
}
`
  }
];

export default function Home() {
  const [files, setFiles] = useState<FileData[]>(initialFiles);
  const [activeFileId, setActiveFileId] = useState<string>("1");
  const [editingFileId, setEditingFileId] = useState<string | null>(null);
  const [editingName, setEditingName] = useState<string>("");
  const [output, setOutput] = useState<string>("");
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<"editor" | "docs">("editor");

  const activeFile = files.find(f => f.id === activeFileId) || files[0];

  const handleEditorWillMount = (monaco: Monaco) => {
    setupGenZLanguage(monaco);
  };

  const handleEditorChange = (value: string | undefined) => {
    if (value !== undefined) {
      setFiles(files.map(f => f.id === activeFileId ? { ...f, content: value } : f));
    }
  };

  const handleCreateFile = () => {
    const newId = Date.now().toString();
    const newFile: FileData = {
      id: newId,
      name: `untitled-${files.length + 1}.genz`,
      content: `// New file\n`
    };
    setFiles([...files, newFile]);
    setActiveFileId(newId);
    setViewMode("editor");
  };

  const handleDeleteFile = (id: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if (files.length <= 1) return; // Cannot delete last file
    const newFiles = files.filter(f => f.id !== id);
    setFiles(newFiles);
    if (activeFileId === id) {
      setActiveFileId(newFiles[0].id);
    }
  };

  const handleStartRename = (file: FileData, e: React.MouseEvent) => {
    e.stopPropagation();
    setEditingFileId(file.id);
    setEditingName(file.name);
  };

  const handleFinishRename = (e?: React.MouseEvent | React.FormEvent) => {
    if (e) e.stopPropagation();
    if (editingFileId && editingName.trim()) {
      setFiles(files.map(f => f.id === editingFileId ? { ...f, name: editingName.trim() } : f));
    }
    setEditingFileId(null);
  };

  const handleRun = async () => {
    setIsRunning(true);
    setOutput("Running...\n");
    try {
      const response = await fetch('/api/run', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: activeFile.content })
      });
      const data = await response.json();
      setOutput(data.output || "Program finished with no output.");
    } catch (err) {
      setOutput("Error connecting to Python backend. Is the Flask server running on port 5000?\n\nDetails: " + String(err));
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div className="flex h-screen text-zinc-50 font-sans selection:bg-zinc-800 bg-[#09090b] relative overflow-hidden">
      {/* Subtle colorful glows for the true Windows 11 Mica effect to blur */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_0%_0%,rgba(99,102,241,0.15),transparent_50%)]"></div>
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_100%_100%,rgba(168,85,247,0.1),transparent_50%)]"></div>

      {/* Sidebar - File Explorer */}
      <aside className="w-64 bg-[#18181b]/50 backdrop-blur-3xl flex flex-col shrink-0 relative z-20">
        <div className="p-4 border-b border-white/10 flex flex-col gap-4">
          <div className="flex items-center gap-2 px-1">
            <h2 className="text-base font-bold tracking-wide text-white uppercase">GenZCode</h2>
          </div>
          
          <div className="flex flex-col gap-1.5">
            <button onClick={handleCreateFile} className="flex items-center gap-2 text-sm text-zinc-400 hover:text-zinc-200 hover:bg-white/5 px-3 py-2 rounded-md transition-colors w-full text-left">
              <FilePlus size={16} />
              New File
            </button>
            <button onClick={() => setViewMode("docs")} className={`flex items-center gap-2 text-sm px-3 py-2 rounded-md transition-colors w-full text-left ${viewMode === 'docs' ? 'bg-white/10 text-white font-medium shadow-sm ring-1 ring-white/5' : 'text-zinc-400 hover:text-zinc-200 hover:bg-white/5'}`}>
              <Book size={16} />
              Documentation
            </button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto py-3 px-3">
          <div className="flex flex-col gap-1">
            {files.map(file => (
              <div
                key={file.id}
                onClick={() => { setActiveFileId(file.id); setViewMode("editor"); }}
                className={`w-full text-left px-3 py-2 text-sm flex items-center justify-between gap-2 transition-colors cursor-pointer group rounded-md ${
                  activeFileId === file.id && viewMode === "editor" ? "bg-white/10 text-white font-medium shadow-sm ring-1 ring-white/5" : "text-zinc-400 hover:bg-white/5 hover:text-zinc-200"
                }`}
              >
                <div className="flex items-center gap-2 overflow-hidden w-full">
                  <FileCode2 size={16} className={activeFileId === file.id ? "text-zinc-100 shrink-0" : "text-zinc-500 shrink-0"} />
                  {editingFileId === file.id ? (
                    <form onSubmit={(e) => { e.preventDefault(); handleFinishRename(); }} className="flex-1 min-w-0">
                      <input
                        autoFocus
                        type="text"
                        value={editingName}
                        onChange={(e) => setEditingName(e.target.value)}
                        onBlur={() => handleFinishRename()}
                        onClick={(e) => e.stopPropagation()}
                        className="w-full bg-zinc-950 border border-zinc-700 rounded px-2 text-zinc-100 text-sm py-1 focus:outline-none focus:border-zinc-500"
                      />
                    </form>
                  ) : (
                    <span className="truncate">{file.name}</span>
                  )}
                </div>

                {!editingFileId && (
                  <div className="flex items-center gap-1.5 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button onClick={(e) => handleStartRename(file, e)} className="p-1 hover:text-zinc-100 text-zinc-500">
                      <Edit2 size={14} />
                    </button>
                    {files.length > 1 && (
                      <button onClick={(e) => handleDeleteFile(file.id, e)} className="p-1 hover:text-red-400 text-zinc-500">
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-transparent relative z-10">

        {/* Header */}
        <header className="flex items-center justify-between px-6 py-3 shrink-0 bg-[#18181b]/50 backdrop-blur-3xl z-10">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-base text-zinc-300 bg-zinc-900/50 px-3 py-1.5 rounded-md border border-zinc-800">
              <FileCode2 size={16} className="text-zinc-400" />
              <span className="font-mono">{activeFile.name}</span>
            </div>
          </div>
          <Button
            onClick={handleRun}
            disabled={isRunning}
            className="bg-zinc-900 text-zinc-100 hover:bg-zinc-800 border border-zinc-700 transition-colors font-medium px-5 h-9 rounded-md shadow-sm flex items-center gap-2"
          >
            <Play size={16} fill="currentColor" />
            {isRunning ? "Running..." : "Run Code"}
          </Button>
        </header>

          {/* Content Area (Editor or Docs) */}
          {viewMode === "editor" ? (
            <div className="flex-1 flex flex-col overflow-hidden bg-[#09090b] rounded-tl-xl border-t border-l border-zinc-800/50 shadow-2xl">

              {/* Editor */}
              <main className="flex-1 overflow-hidden relative">
                <Editor
                  height="100%"
                  language="genz"
                  theme="genzDark"
                  value={activeFile.content}
                  onChange={handleEditorChange}
                  beforeMount={handleEditorWillMount}
                  options={{
                    minimap: { enabled: false },
                    fontSize: 14,
                    fontFamily: "var(--font-geist-mono), ui-monospace, SFMono-Regular, monospace",
                    lineHeight: 1.6,
                    padding: { top: 16, bottom: 16 },
                    scrollBeyondLastLine: false,
                    smoothScrolling: true,
                    cursorBlinking: "smooth",
                    cursorSmoothCaretAnimation: "on",
                    formatOnPaste: true,
                    renderLineHighlight: "all",
                  }}
                />
              </main>

              {/* Output Panel */}
              <div className="h-64 border-t border-white/5 bg-[#050505] flex flex-col shrink-0 relative z-10 shadow-[0_-10px_30px_rgba(0,0,0,0.5)]">
                <div className="px-4 py-2 border-b border-white/5 flex items-center gap-2 text-xs font-medium text-zinc-400 bg-[#0a0a0a] uppercase tracking-wider">
                  <Terminal size={12} />
                  Output
                </div>
                <div className="flex-1 p-4 overflow-y-auto font-mono text-sm text-zinc-300 whitespace-pre-wrap">
                  {output || <span className="text-zinc-600 italic">Ready. Click Run to execute code...</span>}
                </div>
              </div>
            </div>
          ) : (
            <DocsViewer />
          )}

      </div>
    </div>
  );
}
