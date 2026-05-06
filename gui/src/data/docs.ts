export type DocEntry = {
  id: string;
  title: string;
  aliases: string[];
  description: string;
  example: string;
  category: "Output" | "Variables" | "Control Flow" | "Functions" | "Types";
};

export const genzDocs: DocEntry[] = [
  {
    id: "spill_tea",
    title: "spill_tea",
    aliases: ["print", "console.log", "echo", "output"],
    description: "Outputs a value or multiple values to the console. The standard way to display information.",
    example: `spill_tea("Hello world");\nspill_tea("Result:", 42);`,
    category: "Output"
  },
  {
    id: "lowkey",
    title: "lowkey",
    aliases: ["let", "var", "const", "variable", "assign"],
    description: "Declares a new variable. Must be followed by the variable name, a colon, its type, and an initial value.",
    example: `lowkey my_rizz: num = 100;\nlowkey name: txt = "Sigma";`,
    category: "Variables"
  },
  {
    id: "sus",
    title: "sus",
    aliases: ["if", "condition", "branch"],
    description: "An 'if' statement that executes a block of code if the condition evaluates to true.",
    example: `sus (aura > 50) {\n    spill_tea("W");\n}`,
    category: "Control Flow"
  },
  {
    id: "deadass",
    title: "deadass",
    aliases: ["else", "else if", "otherwise", "branch"],
    description: "The 'else' or 'else if' block. Chain it with another 'sus' to create an else-if ladder.",
    example: `sus (x > 10) {\n    spill_tea("Big");\n} deadass sus (x == 10) {\n    spill_tea("Mid");\n} deadass {\n    spill_tea("Small");\n}`,
    category: "Control Flow"
  },
  {
    id: "keep_yapping",
    title: "keep_yapping",
    aliases: ["while", "loop", "iterate", "for"],
    description: "A 'while' loop that continuously executes its block as long as the condition is true.",
    example: `lowkey i: num = 0;\nkeep_yapping (i < 5) {\n    spill_tea(i);\n    i = i + 1;\n}`,
    category: "Control Flow"
  },
  {
    id: "ratio",
    title: "ratio",
    aliases: ["switch", "match", "select"],
    description: "A 'switch' statement. Used alongside 'bet' for cases and 'nvm' for the default case.",
    example: `ratio (grade) {\n    bet "A": {\n        spill_tea("W");\n        bounce;\n    }\n    nvm: {\n        spill_tea("L");\n    }\n}`,
    category: "Control Flow"
  },
  {
    id: "bounce",
    title: "bounce",
    aliases: ["break", "stop", "exit"],
    description: "Breaks out of the current loop or switch case ('ratio' block).",
    example: `keep_yapping (true) {\n    bounce; // Exits immediately\n}`,
    category: "Control Flow"
  },
  {
    id: "next_up",
    title: "next_up",
    aliases: ["continue", "skip"],
    description: "Skips the rest of the current loop iteration and moves to the next one.",
    example: `keep_yapping (i < 10) {\n    i = i + 1;\n    sus (i == 5) {\n        next_up;\n    }\n    spill_tea(i);\n}`,
    category: "Control Flow"
  },
  {
    id: "vibe_check",
    title: "vibe_check",
    aliases: ["function", "def", "fn"],
    description: "Defines a reusable block of code (a function). Can take parameters.",
    example: `vibe_check calculate(a: num, b: num) {\n    slay a + b;\n}`,
    category: "Functions"
  },
  {
    id: "slay",
    title: "slay",
    aliases: ["return", "yield"],
    description: "Returns a value from a function ('vibe_check').",
    example: `vibe_check get_score() {\n    slay 100;\n}`,
    category: "Functions"
  },
  {
    id: "num",
    title: "num",
    aliases: ["number", "int", "integer", "float", "double"],
    description: "The numeric data type in GenZCode. Represents both integers and decimals.",
    example: `lowkey score: num = 99.5;`,
    category: "Types"
  },
  {
    id: "txt",
    title: "txt",
    aliases: ["string", "str", "text", "char"],
    description: "The text/string data type in GenZCode. Enclosed in double quotes.",
    example: `lowkey name: txt = "Skibidi";`,
    category: "Types"
  },
  {
    id: "no_cap",
    title: "no_cap",
    aliases: ["true", "boolean", "yes", "valid"],
    description: "The literal value for 'true' in GenZCode.",
    example: `lowkey is_sigma: num = no_cap;`,
    category: "Types"
  },
  {
    id: "fr_fr",
    title: "fr_fr",
    aliases: ["false", "boolean", "no", "invalid"],
    description: "The literal value for 'false' in GenZCode.",
    example: `lowkey is_mid: num = fr_fr;`,
    category: "Types"
  },
  {
    id: "bet",
    title: "bet",
    aliases: ["case", "match", "option"],
    description: "A 'case' inside a 'ratio' (switch) block.",
    example: `bet "A": {\n    spill_tea("W");\n}`,
    category: "Control Flow"
  },
  {
    id: "nvm",
    title: "nvm",
    aliases: ["default", "else", "fallback"],
    description: "The 'default' case inside a 'ratio' (switch) block if no other 'bet' matches.",
    example: `nvm: {\n    spill_tea("L");\n}`,
    category: "Control Flow"
  }
];
