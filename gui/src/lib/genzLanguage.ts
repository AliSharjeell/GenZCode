import { Monaco } from "@monaco-editor/react";

export function setupGenZLanguage(monaco: Monaco) {
  // Register language
  monaco.languages.register({ id: "genz" });

  // Syntax highlighting
  monaco.languages.setMonarchTokensProvider("genz", {
    keywords: [
      "lowkey", "num", "txt", "sus", "deadass", "keep_yapping",
      "spill_tea", "vibe_check", "slay", "bounce", "next_up",
      "ratio", "bet", "nvm", "no_cap", "fr_fr"
    ],
    operators: [
      "=", ">", "<", "!", "~", "?", ":", "==", "<=", ">=", "!=",
      "&&", "||", "++", "--", "+", "-", "*", "/", "&", "|", "^", "%"
    ],
    tokenizer: {
      root: [
        [/[a-z_$][\w$]*/, { cases: { "@keywords": "keyword", "@default": "identifier" } }],
        [/[0-9]+/, "number"],
        [/[{}()\[\]]/, "@brackets"],
        [/"[^"]*"/, "string"],
        [/\/\/.*/, "comment"],
      ]
    }
  });

  // Autocompletion (Intellisense)
  monaco.languages.registerCompletionItemProvider("genz", {
    provideCompletionItems: (model, position) => {
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
      ];
      return { suggestions };
    }
  });

  // Documentation Hovers
  monaco.languages.registerHoverProvider("genz", {
    provideHover: (model, position) => {
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
        "next_up": "### `next_up`\nSkips the rest of the current iteration and continues to the next."
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
      { token: "keyword", foreground: "e4e4e7" }, // zinc-200
      { token: "identifier", foreground: "a1a1aa" }, // zinc-400
      { token: "number", foreground: "d4d4d8" }, // zinc-300
      { token: "string", foreground: "71717a" }, // zinc-500
      { token: "comment", foreground: "52525b", fontStyle: "italic" }, // zinc-600
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
