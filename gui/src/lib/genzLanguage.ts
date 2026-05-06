import { Monaco } from "@monaco-editor/react";

export function setupGenZLanguage(monaco: Monaco) {
  // Register language
  monaco.languages.register({ id: "genz" });

  // Syntax highlighting
  monaco.languages.setMonarchTokensProvider("genz", {
    controlKeywords: [
      "sus", "deadass", "keep_yapping", "goon", "ratio", "bet", "nvm", "slay", "bounce", "next_up", "edge", "skibidi"
    ],
    typeKeywords: [
      "num", "txt"
    ],
    declKeywords: [
      "lowkey", "vibe_check", "tung_tung_tung_sahur"
    ],
    functionKeywords: [
      "spill_tea", "rizz", "fanum_tax", "mewing", "ohio", "grimace_shake", "ballerina_cappuccina", "skibidi_toilet"
    ],
    boolKeywords: [
      "no_cap", "fr_fr"
    ],
    operators: [
      "=", ">", "<", "!", "~", "?", ":", "==", "<=", ">=", "!=",
      "&&", "||", "++", "--", "+", "-", "*", "/", "&", "|", "^", "%"
    ],
    tokenizer: {
      root: [
        [/[a-z_$][\w$]*/, {
          cases: {
            "@controlKeywords": "keyword.control",
            "@typeKeywords": "type",
            "@declKeywords": "keyword.decl",
            "@functionKeywords": "function",
            "@boolKeywords": "constant",
            "@default": "identifier"
          }
        }],
        [/[0-9]+/, "number"],
        [/[{}()\[\]]/, "@brackets"],
        [/"[^"]*"/, "string"],
        [/\/\/.*/, "comment"],
      ]
    }
  });

  // Autocompletion (Intellisense)
  monaco.languages.registerCompletionItemProvider("genz", {
    provideCompletionItems: (model: any, position: any) => {
      const suggestions = [
        { label: "lowkey", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "lowkey ", detail: "Variable declaration" },
        { label: "num", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "num", detail: "Numeric type" },
        { label: "txt", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "txt", detail: "String type" },
        { label: "sus", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "sus (${1:condition}) {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "If statement" },
        { label: "deadass", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "deadass {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Else branch" },
        { label: "keep_yapping", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "keep_yapping (${1:condition}) {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "While loop" },
        { label: "spill_tea", kind: monaco.languages.CompletionItemKind.Function, insertText: "spill_tea(${1:value});", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Print output" },
        { label: "vibe_check", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "vibe_check ${1:name}(${2:params}) {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Function declaration" },
        { label: "slay", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "slay $0;", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Return value" },
        { label: "bounce", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "bounce;", detail: "Break out of loop" },
        { label: "next_up", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "next_up;", detail: "Continue next iteration" },
        { label: "ratio", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "ratio (${1:expression}) {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Switch statement" },
        { label: "bet", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "bet ${1:case}: {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Case in switch" },
        { label: "nvm", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "nvm: {\n\t$0\n}", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Default case" },
        { label: "no_cap", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "no_cap", detail: "Boolean true" },
        { label: "fr_fr", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "fr_fr", detail: "Boolean false" },
        { label: "tung_tung_tung_sahur", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "tung_tung_tung_sahur", detail: "Wake up / Initialize" },
        { label: "ballerina_cappuccina", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "ballerina_cappuccina", detail: "Graceful exit / Fancy string" },
        { label: "skibidi_toilet", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "skibidi_toilet", detail: "Garbage collection / flush" },
        { label: "skibidi", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "skibidi", detail: "Bad / Evil / Loop" },
        { label: "fanum_tax", kind: monaco.languages.CompletionItemKind.Function, insertText: "fanum_tax(${1:value})", insertTextRules: monaco.languages.CompletionItemInsertTextRule.InsertAsSnippet, detail: "Steal / Subtraction" },
        { label: "rizz", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "rizz", detail: "Charisma / Add / Success" },
        { label: "ohio", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "ohio", detail: "Weird state / Error" },
        { label: "mewing", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "mewing", detail: "Silence / Sleep / Wait" },
        { label: "grimace_shake", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "grimace_shake", detail: "Fatal error / Poison" },
        { label: "goon", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "goon", detail: "Infinite loop" },
        { label: "edge", kind: monaco.languages.CompletionItemKind.Keyword, insertText: "edge", detail: "Almost finish / Yield" },
      ];
      return { suggestions };
    }
  });

  // Documentation Hovers
  monaco.languages.registerHoverProvider("genz", {
    provideHover: (model: any, position: any) => {
      const word = model.getWordAtPosition(position);
      if (!word) return null;
      
      const docs: Record<string, string> = {
        "lowkey": "### `lowkey`\nDeclares a new variable (like `let` or `var`).\n\nExample: `lowkey x: num = 42;`",
        "sus": "### `sus`\nConditional if statement.\n\nExample: `sus (x > 10) { ... }`",
        "deadass": "### `deadass`\nElse branch of a conditional.\n\nExample: `deadass { ... }`",
        "keep_yapping": "### `keep_yapping`\nA while loop that continues as long as the condition is true.\n\nExample: `keep_yapping (x > 0) { ... }`",
        "spill_tea": "### `spill_tea`\nPrints output to the console.\n\nExample: `spill_tea(\"Hello\");`",
        "vibe_check": "### `vibe_check`\nDeclares a function.\n\nExample: `vibe_check factorial(n: num) { ... }`",
        "slay": "### `slay`\nReturns a value from a function.\n\nExample: `slay 42;`",
        "ratio": "### `ratio`\nA switch statement.\n\nExample: `ratio (x) { ... }`",
        "bet": "### `bet`\nA case inside a switch (`ratio`) statement.",
        "nvm": "### `nvm`\nThe default case inside a switch (`ratio`) statement.",
        "no_cap": "### `no_cap`\nBoolean literal representing `true`.",
        "fr_fr": "### `fr_fr`\nBoolean literal representing `false`.",
        "num": "### `num`\nNumeric data type.",
        "txt": "### `txt`\nString data type.",
        "bounce": "### `bounce`\nBreaks out of the current loop.",
        "next_up": "### `next_up`\nSkips the rest of the current iteration and continues to the next.",
        "tung_tung_tung_sahur": "### `tung_tung_tung_sahur`\nTime to wake up your code. Initialize or start a process.",
        "ballerina_cappuccina": "### `ballerina_cappuccina`\nA graceful and fancy operation.",
        "skibidi_toilet": "### `skibidi_toilet`\nFlushes the memory or garbage collection.",
        "skibidi": "### `skibidi`\nSomething chaotic or evil.",
        "fanum_tax": "### `fanum_tax`\nSteals a percentage of a variable's value.",
        "rizz": "### `rizz`\nCharisma. Often used to charm a function into returning true.",
        "ohio": "### `ohio`\nA chaotic state or error condition.",
        "mewing": "### `mewing`\nSilences the output or pauses execution.",
        "grimace_shake": "### `grimace_shake`\nTriggers a fatal error or crash.",
        "goon": "### `goon`\nEnter an infinite loop.",
        "edge": "### `edge`\nYields the current process, coming close to the end but not quite."
      };
      
      if (docs[word.word]) {
        return {
          contents: [{ value: docs[word.word] }]
        };
      }
      return null;
    }
  });

  // Custom Zinc Dark Theme
  monaco.editor.defineTheme("genzDark", {
    base: "vs-dark",
    inherit: true,
    rules: [
      { token: "keyword.control", foreground: "#56b6c2", fontStyle: "bold" }, // Soft Teal/Cyan control flow
      { token: "keyword.decl", foreground: "#e5c07b" },                       // Soft Warm Gold declarations
      { token: "type", foreground: "#4fc1ff" },                               // Soft Light Blue types
      { token: "function", foreground: "#61afef" },                           // Soft Blue functions
      { token: "constant", foreground: "#d19a66" },                           // Soft Amber/Orange booleans/constants
      { token: "identifier", foreground: "#abb2bf" },                         // Soft Slate-white identifiers
      { token: "number", foreground: "#d19a66" },                             // Soft Amber/Orange numbers
      { token: "string", foreground: "#98c379" },                             // Soft Sage Green strings
      { token: "comment", foreground: "#5c6370", fontStyle: "italic" },       // Muted Dark Slate comments
    ],
    colors: {
      "editor.background": "#09090b", // zinc-950
      "editor.foreground": "#f4f4f5", // zinc-100
      "editor.lineHighlightBackground": "#18181b", // zinc-900
      "editorLineNumber.foreground": "#3f3f46", // zinc-700
      "editorIndentGuide.background": "#27272a", // zinc-800
      "editorSuggestWidget.background": "#18181b",
      "editorSuggestWidget.border": "#27272a",
      "editorSuggestWidget.foreground": "#d4d4d8",
      "editorSuggestWidget.selectedBackground": "#27272a",
      "editorHoverWidget.background": "#18181b",
      "editorHoverWidget.border": "#27272a",
    }
  });
}
