import { useState, useMemo } from 'react';
import { Search, BookOpen, Code2 } from 'lucide-react';
import { searchDocs } from '@/lib/search';

export default function DocsViewer() {
  const [query, setQuery] = useState("");

  const results = useMemo(() => searchDocs(query), [query]);

  const categoryColors: Record<string, string> = {
    "Output": "bg-emerald-900/40 text-emerald-400 border-emerald-700/50",
    "Variables": "bg-blue-900/40 text-blue-400 border-blue-700/50",
    "Control Flow": "bg-violet-900/40 text-violet-400 border-violet-700/50",
    "Functions": "bg-amber-900/40 text-amber-400 border-amber-700/50",
    "Types": "bg-cyan-900/40 text-cyan-400 border-cyan-700/50",
    "Operators": "bg-rose-900/40 text-rose-400 border-rose-700/50",
    "Built-in Functions": "bg-sky-900/40 text-sky-400 border-sky-700/50",
    "Brainrot": "bg-fuchsia-900/40 text-fuchsia-400 border-fuchsia-700/50",
  };

  return (
    <div className="flex-1 flex flex-col h-full bg-[#09090b] rounded-tl-xl border-t border-l border-zinc-800/50 shadow-2xl overflow-hidden">
      {/* Docs Header & Search */}
      <div className="p-8 border-b border-white/5 bg-gradient-to-b from-white/[0.02] to-transparent">
        <div className="max-w-3xl mx-auto">
          <h1 className="text-3xl font-medium text-white mb-8 flex items-center justify-center gap-3">
            GenZCode Documentation
          </h1>
        
          <div className="relative group">
            <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-zinc-500 group-focus-within:text-zinc-300 transition-colors">
              <Search size={20} />
            </div>
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search docs (e.g., 'print', 'array', 'loop', 'for')..."
              className="w-full bg-[#18181b]/50 border border-white/10 rounded-full py-4 pl-12 pr-4 text-zinc-100 placeholder-zinc-500 focus:outline-none focus:ring-2 focus:ring-white/10 focus:border-white/10 transition-all shadow-inner backdrop-blur-xl"
            />
          </div>
        </div>
      </div>

      {/* Results Area */}
      <div className="flex-1 overflow-y-auto p-8">
        <div className="max-w-3xl mx-auto space-y-6 pb-20">
          {results.length === 0 ? (
            <div className="text-center py-20 text-zinc-500">
              <p className="text-lg">No results found for &quot;{query}&quot;.</p>
              <p className="text-sm mt-2">Try searching for standard concepts like &quot;variable&quot;, &quot;for&quot;, or &quot;array&quot;.</p>
            </div>
          ) : (
            results.map(doc => (
              <div key={doc.id} className="pb-8 mb-8 border-b border-white/5 last:border-0 last:pb-0 last:mb-0 group">
                <div className="flex items-start justify-between mb-3">
                  <div>
                    <div className="flex items-center gap-3 mb-1">
                      <h3 className="text-xl font-bold text-white font-mono">{doc.title}</h3>
                      <span className={`text-xs font-medium px-2 py-1 rounded border uppercase tracking-wider ${categoryColors[doc.category] || "bg-zinc-800/50 text-zinc-400 border-zinc-700/50"}`}>
                        {doc.category}
                      </span>
                    </div>
                    <div className="text-xs text-zinc-500 flex flex-wrap gap-1 mt-2">
                      <span className="mr-1">Translates:</span>
                      {doc.aliases.map(alias => (
                        <span key={alias} className="bg-white/5 px-1.5 py-0.5 rounded text-zinc-400">
                          {alias}
                        </span>
                      ))}
                    </div>
                  </div>
                </div>
                
                <p className="text-zinc-300 text-sm leading-relaxed mb-4">
                  {doc.description}
                </p>
                
                <div className="bg-black/40 rounded-lg p-4 font-mono text-sm text-zinc-300 border border-white/5 overflow-x-auto relative">
                  <div className="absolute top-0 right-0 p-2 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Code2 size={16} className="text-zinc-500" />
                  </div>
                  <pre><code>{doc.example}</code></pre>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
}
