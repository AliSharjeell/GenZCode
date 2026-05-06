"use client";

import { useState } from "react";
import Editor, { Monaco } from "@monaco-editor/react";
import { setupGenZLanguage } from "@/lib/genzLanguage";
import { Button } from "@/components/ui/button";
import { FileCode2, Plus, Terminal, Play, Trash2, Edit2 } from "lucide-react";

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
tung_tung_tung_sahur

lowkey aura: num = 100;

sus (aura > 50) {
    spill_tea("W rizz");
} deadass {
    skibidi_toilet;
    grimace_shake;
}

ballerina_cappuccina;
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
    <div className="flex h-screen bg-zinc-950 text-zinc-50 font-sans selection:bg-zinc-800">
      
      {/* Sidebar - File Explorer */}
      <aside className="w-64 border-r border-zinc-900 bg-[#09090b] flex flex-col shrink-0">
        <div className="p-4 border-b border-zinc-900 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-zinc-100 text-zinc-950 flex items-center justify-center font-bold text-xs">
              G
            </div>
            <h2 className="text-sm font-semibold tracking-wide text-zinc-300">EXPLORER</h2>
          </div>
          <button onClick={handleCreateFile} className="text-zinc-400 hover:text-zinc-100 transition-colors">
            <Plus size={16} />
          </button>
        </div>
        
        <div className="flex-1 overflow-y-auto py-2">
          {files.map(file => (
            <div
              key={file.id}
              onClick={() => setActiveFileId(file.id)}
              className={`w-full text-left px-4 py-2 text-sm flex items-center justify-between gap-2 transition-colors cursor-pointer group ${
                activeFileId === file.id ? "bg-zinc-900 text-zinc-100 font-medium" : "text-zinc-400 hover:bg-zinc-900/50 hover:text-zinc-300"
              }`}
            >
              <div className="flex items-center gap-2 overflow-hidden w-full">
                <FileCode2 size={14} className={activeFileId === file.id ? "text-zinc-100 shrink-0" : "text-zinc-500 shrink-0"} />
                {editingFileId === file.id ? (
                  <form onSubmit={(e) => { e.preventDefault(); handleFinishRename(); }} className="flex-1 min-w-0">
                    <input
                      autoFocus
                      type="text"
                      value={editingName}
                      onChange={(e) => setEditingName(e.target.value)}
                      onBlur={() => handleFinishRename()}
                      onClick={(e) => e.stopPropagation()}
                      className="w-full bg-zinc-950 border border-zinc-700 rounded px-1 text-zinc-100 text-xs py-0.5 focus:outline-none focus:border-zinc-500"
                    />
                  </form>
                ) : (
                  <span className="truncate">{file.name}</span>
                )}
              </div>
              
              {!editingFileId && (
                <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
                  <button onClick={(e) => handleStartRename(file, e)} className="p-1 hover:text-zinc-100 text-zinc-500">
                    <Edit2 size={12} />
                  </button>
                  {files.length > 1 && (
                    <button onClick={(e) => handleDeleteFile(file.id, e)} className="p-1 hover:text-red-400 text-zinc-500">
                      <Trash2 size={12} />
                    </button>
                  )}
                </div>
              )}
            </div>
          ))}
        </div>
      </aside>

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-zinc-950">
        
        {/* Header */}
        <header className="flex items-center justify-between px-6 py-3 border-b border-zinc-900 bg-zinc-950 shrink-0">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-sm text-zinc-300 bg-zinc-900/50 px-3 py-1.5 rounded-md border border-zinc-800">
              <FileCode2 size={14} className="text-zinc-400" />
              <span className="font-mono">{activeFile.name}</span>
            </div>
          </div>
          <Button 
            onClick={handleRun}
            disabled={isRunning}
            className="bg-zinc-100 text-zinc-900 hover:bg-zinc-200 transition-colors font-medium px-4 h-8 rounded-md shadow-sm flex items-center gap-2"
          >
            <Play size={14} />
            {isRunning ? "Running..." : "Run Code"}
          </Button>
        </header>

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
        <div className="h-64 border-t border-zinc-900 bg-[#09090b] flex flex-col shrink-0">
          <div className="px-4 py-2 border-b border-zinc-900 flex items-center gap-2 text-xs font-medium text-zinc-400 bg-zinc-950/50 uppercase tracking-wider">
            <Terminal size={12} />
            Output
          </div>
          <div className="flex-1 p-4 overflow-y-auto font-mono text-sm text-zinc-300 whitespace-pre-wrap">
            {output || <span className="text-zinc-600 italic">Ready. Click Run to execute code...</span>}
          </div>
        </div>

      </div>
    </div>
  );
}
