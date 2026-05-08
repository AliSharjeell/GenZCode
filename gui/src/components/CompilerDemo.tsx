"use client";

import { useState, useEffect, useCallback } from "react";
import { setupGenZLanguage } from "@/lib/genzLanguage";
import {
  Play, ArrowRight, ArrowLeft, Zap, GitBranch,
  ShieldCheck, FileCode, Terminal, CheckCircle2,
  AlertCircle, RotateCcw, Sparkles, Cpu,
  ChevronRight, BookOpen
} from "lucide-react";

// =============================================================================
// Types
// =============================================================================

type TokenItem = {
  type: string;
  lexeme: string;
  literal: string | number | boolean | null;
  line: number;
  column: number;
};

type ASTNode = {
  _type: string;
  [key: string]: any;
};

type PipelineData = {
  stages: {
    name: string;
    title: string;
    description: string;
    status: string;
    error?: string;
    tokens?: TokenItem[];
    ast?: ASTNode;
    symbol_table?: { scopes: { name: string; symbols: Record<string, any> }[] };
    python_code?: string;
    output?: string;
  }[];
  error: string | null;
  output: string;
};

// =============================================================================
// Short Demo Code
// =============================================================================

const DEMO_CODE = `// Check passing grade
lowkey score: num = 85;

sus (score >= 60) {
    spill_tea("Passed! No cap.");
}`;

// =============================================================================
// Stage Metadata
// =============================================================================

const STAGES = [
  {
    key: "intro",
    title: "Welcome",
    subtitle: "Compiler Pipeline Tour",
    icon: Sparkles,
    color: "#f59e0b",
    bg: "rgba(245,158,11,0.08)",
  },
  {
    key: "lexer",
    title: "Step 1: Lexical Analysis",
    subtitle: "Breaking code into tokens",
    icon: Zap,
    color: "#f59e0b",
    bg: "rgba(245,158,11,0.08)",
    explanation: "The Lexer (or Tokenizer) reads the raw source code character by character and groups them into meaningful units called tokens. It strips comments and whitespace, recognizes keywords like lowkey and sus, identifies numbers, strings, operators, and punctuation.",
  },
  {
    key: "parser",
    title: "Step 2: Syntax Analysis",
    subtitle: "Building the Abstract Syntax Tree",
    icon: GitBranch,
    color: "#8b5cf6",
    bg: "rgba(139,92,246,0.08)",
    explanation: "The Parser takes the token stream and constructs an Abstract Syntax Tree (AST). It validates that the code follows the language grammar rules, handles operator precedence, and builds a hierarchical tree structure that represents the program's logic.",
  },
  {
    key: "semantic",
    title: "Step 3: Semantic Analysis",
    subtitle: "Checking types and scopes",
    icon: ShieldCheck,
    color: "#10b981",
    bg: "rgba(16,185,129,0.08)",
    explanation: "The Semantic Analyzer walks the AST to ensure the program makes sense. It checks that variables are declared before use, types match in assignments and expressions, function calls have valid arguments, and that control flow statements like bounce appear inside loops.",
  },
  {
    key: "generator",
    title: "Step 4: Code Generation",
    subtitle: "Translating to Python",
    icon: FileCode,
    color: "#3b82f6",
    bg: "rgba(59,130,246,0.08)",
    explanation: "The Code Generator traverses the validated AST and emits equivalent Python code. GenZ keywords are mapped to Python constructs: lowkey becomes a variable assignment, sus becomes an if statement, keep_yapping becomes a while loop, and vibe_check becomes a function definition.",
  },
  {
    key: "interpreter",
    title: "Step 5: Execution",
    subtitle: "Running the program",
    icon: Terminal,
    color: "#ec4899",
    bg: "rgba(236,72,153,0.08)",
    explanation: "The Interpreter walks the AST and executes it directly. It maintains an environment to store variables, evaluates expressions with proper operator semantics, handles function calls, and produces the final program output.",
  },
  {
    key: "summary",
    title: "Tour Complete",
    subtitle: "You have seen the full pipeline",
    icon: CheckCircle2,
    color: "#10b981",
    bg: "rgba(16,185,129,0.08)",
  },
];

// =============================================================================
// Token Colors
// =============================================================================

const TOKEN_COLORS: Record<string, string> = {
  LOWKEY: "#e5c07b", NUM: "#4fc1ff", TXT: "#4fc1ff",
  SUS: "#56b6c2", DEADASS: "#56b6c2", KEEP_YAPPING: "#56b6c2",
  SPILL_TEA: "#61afef", VIBE_CHECK: "#e5c07b", SLAY: "#56b6c2",
  BOUNCE: "#56b6c2", NEXT_UP: "#56b6c2", NO_CAP: "#d19a66",
  FR_FR: "#d19a66", RATIO: "#56b6c2", BET: "#56b6c2", NVM: "#56b6c2",
  IDENT: "#abb2bf", NUMBER: "#d19a66", STRING: "#98c379",
  PLUS: "#abb2bf", MINUS: "#abb2bf", STAR: "#abb2bf", SLASH: "#abb2bf",
  PERCENT: "#abb2bf", ASSIGN: "#abb2bf", EQ: "#abb2bf", NEQ: "#abb2bf",
  LT: "#abb2bf", GT: "#abb2bf", LTE: "#abb2bf", GTE: "#abb2bf",
  AND: "#56b6c2", OR: "#56b6c2", NOT: "#56b6c2",
  LPAREN: "#abb2bf", RPAREN: "#abb2bf", LBRACE: "#abb2bf", RBRACE: "#abb2bf",
  LBRACKET: "#abb2bf", RBRACKET: "#abb2bf", SEMI: "#abb2bf",
  COMMA: "#abb2bf", COLON: "#abb2bf", EOF: "#5c6370",
};

function tc(type: string) { return TOKEN_COLORS[type] || "#abb2bf"; }

// =============================================================================
// Visual Components
// =============================================================================

function TokenBadge({ token, delay }: { token: TokenItem; delay: number }) {
  return (
    <div
      className="flex flex-col items-center gap-1 px-3 py-2 rounded-lg border animate-in fade-in zoom-in-95 duration-500"
      style={{
        backgroundColor: `${tc(token.type)}10`,
        borderColor: `${tc(token.type)}30`,
        animationDelay: `${delay}ms`,
        animationFillMode: "both",
      }}
    >
      <span className="text-[10px] font-bold uppercase tracking-wider" style={{ color: tc(token.type) }}>
        {token.type}
      </span>
      <span className="text-xs font-mono text-zinc-200">{token.lexeme}</span>
      {token.literal !== null && token.literal !== token.lexeme && (
        <span className="text-[9px] text-zinc-500 font-mono">= {String(token.literal)}</span>
      )}
    </div>
  );
}

function ASTNodeView({ node, depth = 0 }: { node: ASTNode | null; depth?: number }) {
  if (!node || typeof node !== "object") {
    return <span className="text-xs font-mono text-amber-400">{node === null ? "null" : String(node)}</span>;
  }
  const [expanded, setExpanded] = useState(depth < 1);
  const typeName = node._type || "Unknown";
  const children = Object.entries(node).filter(([k]) => k !== "_type");
  const hasChildren = children.length > 0;
  const isLeaf = !hasChildren || children.every(([, v]) => typeof v !== "object" || v === null);

  const colorMap: Record<string, string> = {
    Program: "#f59e0b", VarDecl: "#8b5cf6", FuncDecl: "#8b5cf6",
    PrintStmt: "#10b981", IfStmt: "#10b981", WhileStmt: "#10b981",
    Binary: "#3b82f6", Unary: "#3b82f6", Literal: "#3b82f6",
    Variable: "#3b82f6", ArrayAccess: "#3b82f6", FuncCall: "#3b82f6",
    Assignment: "#3b82f6", Block: "#10b981",
  };

  return (
    <div className="flex flex-col">
      <button
        onClick={() => hasChildren && setExpanded(!expanded)}
        className="flex items-center gap-1 text-left hover:bg-white/[0.03] rounded px-1 py-0.5 transition-colors"
        style={{ paddingLeft: `${depth * 20}px` }}
      >
        {hasChildren && !isLeaf ? (
          expanded ? <ChevronRight size={10} className="text-zinc-500 rotate-90 transition-transform" />
            : <ChevronRight size={10} className="text-zinc-500 transition-transform" />
        ) : <div className="w-[10px] shrink-0" />}
        <span className="text-xs font-bold" style={{ color: colorMap[typeName] || "#d4d4d8" }}>{typeName}</span>
        {isLeaf && children.length > 0 && (
          <span className="text-[10px] text-zinc-600 ml-1">
            {children.map(([k, v]) => `${k}: ${typeof v === "string" ? `"${v}"` : String(v)}`).join(", ")}
          </span>
        )}
      </button>
      {expanded && hasChildren && !isLeaf && (
        <div className="flex flex-col">
          {children.map(([key, value]) => (
            <div key={key} className="flex items-start gap-2 text-left" style={{ paddingLeft: `${(depth + 1) * 20}px` }}>
              <span className="text-[10px] font-mono text-zinc-600 mt-0.5 shrink-0">{key}:</span>
              {Array.isArray(value) ? (
                <div className="flex flex-col">
                  {value.length === 0 ? <span className="text-[10px] text-zinc-600">[]</span>
                    : value.map((item, i) => <ASTNodeView key={i} node={item} depth={depth + 2} />)}
                </div>
              ) : <ASTNodeView node={value} depth={depth + 2} />}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

function CodeBlock({ code, label, accent }: { code: string; label: string; accent: string }) {
  const lines = code.split("\n");
  return (
    <div className="flex flex-col rounded-xl overflow-hidden border" style={{ borderColor: `${accent}20`, backgroundColor: "#0c0c0e" }}>
      <div className="flex items-center gap-2 px-4 py-2.5" style={{ backgroundColor: `${accent}08`, borderBottom: `1px solid ${accent}15` }}>
        <div className="w-2 h-2 rounded-full" style={{ backgroundColor: accent }} />
        <span className="text-[11px] font-medium uppercase tracking-wider" style={{ color: accent }}>{label}</span>
      </div>
      <div className="overflow-x-auto p-4">
        <div className="flex flex-col gap-0.5">
          {lines.map((line, i) => (
            <div key={i} className="flex items-start gap-3">
              <span className="text-[10px] text-zinc-700 font-mono w-5 text-right shrink-0 select-none">{i + 1}</span>
              <span className="text-xs font-mono text-zinc-300 whitespace-pre">{line || " "}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

function TerminalBlock({ output }: { output: string }) {
  return (
    <div className="flex flex-col rounded-xl overflow-hidden border border-pink-500/20 bg-[#0c0c0e]">
      <div className="flex items-center gap-2 px-4 py-2.5 bg-pink-500/5 border-b border-pink-500/10">
        <Terminal size={12} className="text-pink-400" />
        <span className="text-[11px] font-medium text-pink-400 uppercase tracking-wider">Program Output</span>
      </div>
      <div className="p-4 font-mono text-sm text-zinc-300 min-h-[60px]">
        {output ? (
          <span className="text-emerald-400">{output}</span>
        ) : (
          <span className="text-zinc-600 italic">No output produced.</span>
        )}
      </div>
    </div>
  );
}

// =============================================================================
// Main Component
// =============================================================================

export default function CompilerDemo() {
  const [step, setStep] = useState(0);
  const [data, setData] = useState<PipelineData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const totalSteps = STAGES.length;
  const stageMeta = STAGES[step];
  const stageData = data?.stages?.[step - 1];

  const startTour = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await fetch("/api/pipeline", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code: DEMO_CODE }),
      });
      const json = await res.json();
      if (json.error && !json.stages?.length) {
        setError(json.error);
      } else {
        setData(json);
        setStep(1);
      }
    } catch (e) {
      setError("Could not connect to the compiler backend. Make sure the server is running.");
    } finally {
      setLoading(false);
    }
  };

  const nextStep = () => {
    if (step < totalSteps - 1) setStep(step + 1);
  };

  const prevStep = () => {
    if (step > 0) setStep(step - 1);
  };

  const goToStep = (i: number) => {
    if (data || i === 0) setStep(i);
  };

  const resetTour = () => {
    setStep(0);
    setData(null);
    setError(null);
  };

  // Keyboard navigation
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "ArrowRight" && step > 0 && step < totalSteps - 1) {
        nextStep();
      }
      if (e.key === "ArrowLeft" && step > 1) {
        prevStep();
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [step, totalSteps]);

  // ===================== INTRO SCREEN =====================
  if (step === 0) {
    return (
      <div className="flex-1 flex items-center justify-center bg-[#09090b] rounded-tl-xl border-t border-l border-zinc-800/50 shadow-2xl p-8">
        <div className="flex flex-col items-center text-center gap-8 max-w-lg w-full">
          {/* Animated rings */}
          <div className="relative w-24 h-24 flex items-center justify-center">
            <div className="absolute inset-0 rounded-full border border-amber-500/20 animate-[spin_8s_linear_infinite]" />
            <div className="absolute inset-2 rounded-full border border-violet-500/20 animate-[spin_6s_linear_infinite_reverse]" />
            <div className="absolute inset-4 rounded-full border border-emerald-500/20 animate-[spin_4s_linear_infinite]" />
            <div className="relative w-12 h-12 rounded-xl bg-gradient-to-br from-amber-500/20 to-violet-500/20 border border-white/10 flex items-center justify-center">
              <Cpu size={24} className="text-zinc-200" />
            </div>
          </div>

          <div className="flex flex-col gap-3">
            <h2 className="text-2xl font-semibold text-zinc-100">Compiler Pipeline Tour</h2>
            <p className="text-sm text-zinc-500 leading-relaxed">
              See exactly how GenZCode transforms your source code into a running program.
              We will walk through each compiler stage step by step with a simple example.
            </p>
          </div>

          {/* Preview the demo code */}
          <div className="w-full">
            <div className="text-[10px] font-medium text-zinc-600 uppercase tracking-wider mb-2 text-left">Demo Code</div>
            <CodeBlock code={DEMO_CODE} label="GenZ Source" accent="#f59e0b" />
          </div>

          <div className="flex flex-col gap-3 w-full">
            {error && (
              <div className="p-3 rounded-lg bg-red-500/5 border border-red-500/20 text-xs text-red-400 text-left">
                {error}
              </div>
            )}
            <button
              onClick={startTour}
              disabled={loading}
              className="flex items-center justify-center gap-2 w-full py-3 rounded-xl bg-zinc-100 text-zinc-900 font-medium text-sm hover:bg-white transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="w-4 h-4 border-2 border-zinc-400 border-t-transparent rounded-full animate-spin" />
                  Compiling...
                </>
              ) : (
                <>
                  <Play size={16} fill="currentColor" />
                  Start Compiler Tour
                </>
              )}
            </button>
            <p className="text-[11px] text-zinc-600">
              This will run the compiler pipeline and guide you through 5 stages.
            </p>
          </div>
        </div>
      </div>
    );
  }

  // ===================== SUMMARY SCREEN =====================
  if (step === totalSteps - 1) {
    return (
      <div className="flex-1 flex items-center justify-center bg-[#09090b] rounded-tl-xl border-t border-l border-zinc-800/50 shadow-2xl p-8">
        <div className="flex flex-col items-center text-center gap-8 max-w-lg w-full animate-in fade-in zoom-in-95 duration-500">
          <div className="w-20 h-20 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center">
            <CheckCircle2 size={36} className="text-emerald-400" />
          </div>

          <div className="flex flex-col gap-3">
            <h2 className="text-2xl font-semibold text-zinc-100">Tour Complete!</h2>
            <p className="text-sm text-zinc-500 leading-relaxed">
              You have seen how GenZCode is processed from raw source code all the way to execution.
              The compiler pipeline ensures your code is valid, well-structured, and ready to run.
            </p>
          </div>

          {/* Pipeline summary */}
          <div className="w-full flex flex-col gap-2">
            {STAGES.slice(1, -1).map((s, i) => (
              <div key={s.key} className="flex items-center gap-3 p-3 rounded-lg border border-white/5 bg-white/[0.02]">
                <div className="w-8 h-8 rounded-lg flex items-center justify-center" style={{ backgroundColor: s.bg }}>
                  <s.icon size={16} style={{ color: s.color }} />
                </div>
                <div className="text-left">
                  <div className="text-xs font-medium text-zinc-200">{s.title}</div>
                  <div className="text-[10px] text-zinc-500">{s.subtitle}</div>
                </div>
                <CheckCircle2 size={14} className="ml-auto text-emerald-400/60" />
              </div>
            ))}
          </div>

          <button
            onClick={resetTour}
            className="flex items-center gap-2 px-6 py-2.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-zinc-300 text-sm font-medium transition-colors"
          >
            <RotateCcw size={14} />
            Run Tour Again
          </button>
        </div>
      </div>
    );
  }

  // ===================== STAGE SCREENS =====================
  const tokens = stageData?.tokens?.filter((t) => t.type !== "EOF") || [];
  const ast = stageData?.ast || null;
  const symTable = stageData?.symbol_table || null;
  const pyCode = stageData?.python_code || "";
  const execOutput = stageData?.output || "";
  const hasError = stageData?.status === "error";

  return (
    <div className="flex-1 flex flex-col bg-[#09090b] rounded-tl-xl border-t border-l border-zinc-800/50 shadow-2xl overflow-hidden">
      {/* Top bar */}
      <div className="shrink-0 px-6 py-4 border-b border-white/5 bg-[#0c0c0e]/80 backdrop-blur-3xl">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div
              className="w-9 h-9 rounded-lg flex items-center justify-center border"
              style={{ backgroundColor: stageMeta.bg, borderColor: `${stageMeta.color}25` }}
            >
              <stageMeta.icon size={18} style={{ color: stageMeta.color }} />
            </div>
            <div>
              <h2 className="text-sm font-medium text-zinc-100">{stageMeta.title}</h2>
              <p className="text-[11px] text-zinc-500">{stageMeta.subtitle}</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={prevStep}
              disabled={step <= 1}
              className="flex items-center gap-1 px-3 py-2 rounded-lg text-xs font-medium text-zinc-400 hover:text-zinc-200 hover:bg-white/5 transition-colors disabled:opacity-30 disabled:cursor-not-allowed"
            >
              <ArrowLeft size={14} /> Previous
            </button>
            <button
              onClick={nextStep}
              className="flex items-center gap-1 px-4 py-2 rounded-lg text-xs font-medium bg-zinc-100 text-zinc-900 hover:bg-white transition-colors"
            >
              {step === totalSteps - 2 ? "Finish" : "Next"}
              <ArrowRight size={14} />
            </button>
          </div>
        </div>
      </div>

      {/* Progress dots */}
      <div className="shrink-0 flex items-center justify-center gap-2 py-3 border-b border-white/5 bg-[#0a0a0a]">
        {STAGES.map((s, i) => (
          <button
            key={s.key}
            onClick={() => goToStep(i)}
            className="group relative flex items-center gap-1 transition-all"
          >
            <div
              className={`w-2.5 h-2.5 rounded-full transition-all duration-300 ${
                i === step ? "scale-125" : i < step ? "opacity-100" : "opacity-30"
              }`}
              style={{
                backgroundColor: i === step ? stageMeta.color : i < step ? "#10b981" : "#52525b",
                boxShadow: i === step ? `0 0 12px ${stageMeta.color}40` : "none",
              }}
            />
            {i === step && (
              <span className="text-[10px] font-medium text-zinc-400 ml-1 transition-all">
                Step {i} of {totalSteps - 2}
              </span>
            )}
          </button>
        ))}
      </div>

      {/* Main content */}
      <div className="flex-1 overflow-y-auto">
        <div className="flex flex-col gap-6 p-6 max-w-5xl mx-auto">
          {/* Explanation card */}
          <div
            className="p-5 rounded-xl border animate-in fade-in slide-in-from-bottom-4 duration-500"
            style={{ backgroundColor: `${stageMeta.color}06`, borderColor: `${stageMeta.color}15` }}
          >
            <div className="flex items-start gap-3">
              <BookOpen size={16} className="shrink-0 mt-0.5" style={{ color: stageMeta.color }} />
              <p className="text-sm text-zinc-400 leading-relaxed">
                {(stageMeta as any).explanation}
              </p>
            </div>
          </div>

          {/* Stage-specific content */}
          <div className="animate-in fade-in slide-in-from-bottom-6 duration-700">
            {/* LEXER */}
            {stageMeta.key === "lexer" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Source Code</h3>
                  <CodeBlock code={DEMO_CODE} label="Input" accent="#f59e0b" />
                </div>
                <div className="flex flex-col gap-2">
                  <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">
                    Tokens ({tokens.length} found)
                  </h3>
                  <div className="flex flex-wrap gap-2 p-4 rounded-xl border border-white/5 bg-[#0c0c0e]">
                    {tokens.map((t, i) => (
                      <TokenBadge key={i} token={t} delay={i * 80} />
                    ))}
                  </div>
                </div>
                <div className="p-4 rounded-xl border border-white/5 bg-white/[0.02]">
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    Each colored box above is a <strong className="text-zinc-300">token</strong>. Notice how
                    <span className="text-amber-400"> lowkey</span> becomes a <span className="font-mono text-amber-400">LOWKEY</span> token,
                    <span className="text-blue-400"> score</span> becomes an <span className="font-mono text-blue-400">IDENT</span> token,
                    and <span className="text-orange-400">85</span> becomes a <span className="font-mono text-orange-400">NUMBER</span> token with literal value 85.
                  </p>
                </div>
              </div>
            )}

            {/* PARSER */}
            {stageMeta.key === "parser" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Abstract Syntax Tree</h3>
                  <div className="p-4 rounded-xl border border-violet-500/10 bg-violet-500/[0.02] overflow-x-auto">
                    {ast ? <ASTNodeView node={ast} /> : <span className="text-xs text-zinc-600">No AST data.</span>}
                  </div>
                </div>
                <div className="p-4 rounded-xl border border-white/5 bg-white/[0.02]">
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    The AST is a tree where the root is a <strong className="text-amber-400">Program</strong> node.
                    It contains a <strong className="text-violet-400">VarDecl</strong> (variable declaration) and an
                    <strong className="text-emerald-400"> IfStmt</strong> (conditional). The IfStmt contains a
                    <strong className="text-blue-400"> Binary</strong> comparison (<code className="text-zinc-400">&gt;=</code>) and a
                    <strong className="text-emerald-400"> PrintStmt</strong> inside its then-branch.
                  </p>
                </div>
              </div>
            )}

            {/* SEMANTIC */}
            {stageMeta.key === "semantic" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Symbol Table</h3>
                  {symTable ? (
                    <div className="flex flex-col gap-3">
                      {symTable.scopes.map((scope, i) => (
                        <div key={i} className="flex flex-col gap-2 p-4 rounded-xl border border-emerald-500/10 bg-emerald-500/[0.02]">
                          <div className="flex items-center gap-2">
                            <ShieldCheck size={14} className="text-emerald-400" />
                            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider">{scope.name} Scope</span>
                            <span className="text-[10px] text-zinc-600">{Object.keys(scope.symbols).length} symbols</span>
                          </div>
                          <div className="grid grid-cols-2 md:grid-cols-3 gap-2">
                            {Object.values(scope.symbols).slice(0, 6).map((sym: any, j) => (
                              <div key={j} className="flex items-center justify-between p-2.5 rounded-lg bg-white/[0.03] border border-white/5">
                                <span className="text-xs font-mono text-zinc-200">{sym.name}</span>
                                <span className="text-[10px] px-1.5 py-0.5 rounded bg-white/5 text-zinc-400 font-mono">{sym.type}</span>
                              </div>
                            ))}
                          </div>
                          {Object.keys(scope.symbols).length > 6 && (
                            <span className="text-[10px] text-zinc-600">...and {Object.keys(scope.symbols).length - 6} more built-ins</span>
                          )}
                        </div>
                      ))}
                    </div>
                  ) : (
                    <span className="text-xs text-zinc-600">No symbol table data.</span>
                  )}
                </div>
                <div className="p-4 rounded-xl border border-white/5 bg-white/[0.02]">
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    The symbol table tracks every variable and function. Here, <strong className="text-zinc-300">score</strong> is registered
                    as a <code className="text-zinc-400">num</code> in the global scope. Built-in functions like
                    <code className="text-zinc-400"> print</code> and <code className="text-zinc-400">len</code> are also registered so the analyzer
                    knows they are valid when called.
                  </p>
                </div>
              </div>
            )}

            {/* GENERATOR */}
            {stageMeta.key === "generator" && (
              <div className="flex flex-col gap-6">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="flex flex-col gap-2">
                    <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">GenZ Source</h3>
                    <CodeBlock code={DEMO_CODE} label="Input" accent="#f59e0b" />
                  </div>
                  <div className="flex flex-col gap-2">
                    <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Generated Python</h3>
                    <CodeBlock code={pyCode} label="Output" accent="#3b82f6" />
                  </div>
                </div>
                <div className="p-4 rounded-xl border border-white/5 bg-white/[0.02]">
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    Notice the transformations: <code className="text-amber-400">lowkey score: num = 85</code> becomes
                    <code className="text-blue-400"> score = 85</code>, and <code className="text-emerald-400">sus (score &gt;= 60)</code> becomes
                    <code className="text-blue-400"> if score &gt;= 60</code>. The generator also includes helper functions for brainrot builtins.
                  </p>
                </div>
              </div>
            )}

            {/* INTERPRETER */}
            {stageMeta.key === "interpreter" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-col gap-2">
                  <h3 className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Execution Result</h3>
                  <TerminalBlock output={execOutput} />
                </div>
                <div className="p-4 rounded-xl border border-white/5 bg-white/[0.02]">
                  <p className="text-xs text-zinc-500 leading-relaxed">
                    The interpreter executed the AST directly. It created the variable <code className="text-zinc-400">score</code> with value
                    <code className="text-orange-400"> 85</code>, evaluated the condition <code className="text-zinc-400">85 &gt;= 60</code> as true,
                    and ran the <code className="text-emerald-400">spill_tea</code> statement to print the result.
                  </p>
                </div>
              </div>
            )}

            {hasError && stageData?.error && (
              <div className="p-4 rounded-xl bg-red-500/5 border border-red-500/20">
                <div className="flex items-center gap-2 mb-2">
                  <AlertCircle size={14} className="text-red-400" />
                  <span className="text-xs font-medium text-red-400">Stage Error</span>
                </div>
                <p className="text-xs text-zinc-400 font-mono">{stageData.error}</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
