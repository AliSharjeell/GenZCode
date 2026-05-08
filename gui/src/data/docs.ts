export type DocEntry = {
  id: string;
  title: string;
  aliases: string[];
  description: string;
  example: string;
  category: "Output" | "Variables" | "Control Flow" | "Functions" | "Types" | "Operators" | "Built-in Functions" | "Brainrot";
};

export const genzDocs: DocEntry[] = [
  // ─── Output ──────────────────────────────────────────
  {
    id: "spill_tea",
    title: "spill_tea",
    aliases: ["print", "console.log", "echo", "output"],
    description: "Outputs a value or multiple values to the console. The standard way to display information.",
    example: `spill_tea("Hello world");\nspill_tea("Result:", 42);`,
    category: "Output"
  },

  // ─── Variables ───────────────────────────────────────
  {
    id: "lowkey",
    title: "lowkey",
    aliases: ["let", "var", "const", "variable", "assign", "declare"],
    description: "Declares a new variable. Must be followed by the variable name, a colon, its type, and an optional initial value.",
    example: `lowkey my_rizz: num = 100;\nlowkey name: txt = "Sigma";\nlowkey scores: num[] = [1, 2, 3];`,
    category: "Variables"
  },

  // ─── Types ───────────────────────────────────────────
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
    description: "The text/string data type in GenZCode. Enclosed in double quotes. Supports escape sequences: \\n, \\t, \\\\, \\\", \\r, \\0.",
    example: `lowkey name: txt = "Skibidi";\nlowkey quote: txt = "She said \\"hello\\"\\nNew line";`,
    category: "Types"
  },
  {
    id: "num_array",
    title: "num[]",
    aliases: ["array", "list", "num array"],
    description: "An array of numeric values. Declared with the [] suffix. Elements are accessed with bracket notation and zero-based indexing.",
    example: `lowkey scores: num[] = [10, 20, 30];\nspill_tea(scores[0]); // 10\nscores[1] = 99;`,
    category: "Types"
  },
  {
    id: "txt_array",
    title: "txt[]",
    aliases: ["string array", "text array", "string list"],
    description: "An array of text/string values. Declared with the [] suffix.",
    example: `lowkey names: txt[] = ["Alice", "Bob"];\nspill_tea(names[0]);`,
    category: "Types"
  },
  {
    id: "no_cap",
    title: "no_cap",
    aliases: ["true", "boolean", "yes", "valid"],
    description: "The literal value for 'true' in GenZCode. Stored as a num type.",
    example: `lowkey is_sigma: num = no_cap;`,
    category: "Types"
  },
  {
    id: "fr_fr",
    title: "fr_fr",
    aliases: ["false", "boolean", "no", "invalid"],
    description: "The literal value for 'false' in GenZCode. Stored as a num type.",
    example: `lowkey is_mid: num = fr_fr;`,
    category: "Types"
  },

  // ─── Control Flow ────────────────────────────────────
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
    example: `sus (x > 10) {\n    spill_tea("Big");\n} deadass sus (x > 5) {\n    spill_tea("Medium");\n} deadass {\n    spill_tea("Small");\n}`,
    category: "Control Flow"
  },
  {
    id: "keep_yapping",
    title: "keep_yapping",
    aliases: ["while", "loop", "iterate"],
    description: "A 'while' loop that continuously executes its block as long as the condition is true.",
    example: `lowkey i: num = 0;\nkeep_yapping (i < 5) {\n    spill_tea(i);\n    i = i + 1;\n}`,
    category: "Control Flow"
  },
  {
    id: "yapping_through",
    title: "yapping_through",
    aliases: ["for", "for loop", "c-style for"],
    description: "A C-style 'for' loop with an initializer, condition, and update expression. The initializer can declare a variable with 'lowkey'.",
    example: `yapping_through (lowkey i: num = 0; i < 5; i = i + 1) {\n    spill_tea(i);\n}`,
    category: "Control Flow"
  },
  {
    id: "goon",
    title: "goon",
    aliases: ["infinite loop", "forever", "while true"],
    description: "Enter an infinite loop. Equivalent to 'while true'. Use 'bounce' to break out.",
    example: `lowkey count: num = 0;\ngoon {\n    spill_tea(count);\n    count = count + 1;\n    sus (count >= 5) {\n        bounce;\n    }\n}`,
    category: "Control Flow"
  },
  {
    id: "ratio",
    title: "ratio",
    aliases: ["switch", "match", "select"],
    description: "A 'switch' statement. Used alongside 'bet' for cases and 'nvm' for the default case.",
    example: `ratio (grade) {\n    bet "A": {\n        spill_tea("W");\n    }\n    bet "B": {\n        spill_tea("Valid");\n    }\n    nvm: {\n        spill_tea("L");\n    }\n}`,
    category: "Control Flow"
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
  },
  {
    id: "bounce",
    title: "bounce",
    aliases: ["break", "stop", "exit", "bestie"],
    description: "Breaks out of the current loop or switch case ('ratio' block). 'bestie' is an alias.",
    example: `keep_yapping (no_cap) {\n    sus (found) {\n        bounce; // Exits loop\n    }\n}`,
    category: "Control Flow"
  },
  {
    id: "next_up",
    title: "next_up",
    aliases: ["continue", "skip", "its_giving"],
    description: "Skips the rest of the current loop iteration and moves to the next one. 'its_giving' is an alias.",
    example: `keep_yapping (i < 10) {\n    i = i + 1;\n    sus (i == 5) {\n        next_up;\n    }\n    spill_tea(i);\n}`,
    category: "Control Flow"
  },
  {
    id: "vibe_check",
    title: "vibe_check",
    aliases: ["function", "def", "fn"],
    description: "Defines a reusable block of code (a function). Can take typed parameters and return values with 'slay'.",
    example: `vibe_check calculate(a: num, b: num) {\n    slay a + b;\n}\nspill_tea(calculate(3, 4));`,
    category: "Functions"
  },
  {
    id: "slay",
    title: "slay",
    aliases: ["return", "yield"],
    description: "Returns a value from a function ('vibe_check'). Can also be used without a value for early exit.",
    example: `vibe_check get_score() {\n    slay 100;\n}\n\nvibe_check early_exit() {\n    slay;\n}`,
    category: "Functions"
  },

  // ─── Operators ───────────────────────────────────────
  {
    id: "arithmetic",
    title: "Arithmetic Operators",
    aliases: ["+", "-", "*", "/", "%", "add", "subtract", "multiply", "divide", "modulo", "math"],
    description: "Standard arithmetic operators: + (add), - (subtract), * (multiply), / (divide), % (modulo). The + operator also concatenates strings.",
    example: `lowkey sum: num = 10 + 5;\nlowkey diff: num = 10 - 5;\nlowkey prod: num = 10 * 5;\nlowkey quot: num = 10 / 5;\nlowkey mod: num = 10 % 3;`,
    category: "Operators"
  },
  {
    id: "comparison",
    title: "Comparison Operators",
    aliases: ["==", "!=", "<", ">", "<=", ">=", "equal", "compare", "less", "greater"],
    description: "Comparison operators: == (equal), != (not equal), < (less than), > (greater than), <= (less or equal), >= (greater or equal).",
    example: `lowkey a: num = 10;\nlowkey b: num = 5;\nlowkey eq: num = a == b;\nlowkey gt: num = a > b;`,
    category: "Operators"
  },
  {
    id: "logical",
    title: "Logical Operators",
    aliases: ["&&", "||", "!", "and", "or", "not", "logical"],
    description: "Logical operators: && (and), || (or), ! (not). Used to combine boolean expressions.",
    example: `lowkey result: num = no_cap && fr_fr;\nlowkey either: num = no_cap || fr_fr;\nlowkey negated: num = !no_cap;`,
    category: "Operators"
  },
  {
    id: "assignment",
    title: "Assignment",
    aliases: ["=", "assign", "set", "store"],
    description: "The = operator assigns a value to a variable. Use it after declaration with 'lowkey' to update the variable.",
    example: `lowkey x: num = 10;\nx = 20;\nlowkey arr: num[] = [1, 2, 3];\narr[0] = 99;`,
    category: "Operators"
  },

  // ─── Built-in Functions ──────────────────────────────
  {
    id: "len",
    title: "len",
    aliases: ["length", "size", "count"],
    description: "Returns the length of an array or string.",
    example: `lowkey arr: num[] = [10, 20, 30];\nspill_tea(len(arr)); // 3\nlowkey name: txt = "hello";\nspill_tea(len(name)); // 5`,
    category: "Built-in Functions"
  },
  {
    id: "range",
    title: "range",
    aliases: ["sequence", "numbers", "for range"],
    description: "Generates a list of numbers. Can take 1 arg (0..n), 2 args (start..end), or 3 args (start..end, step).",
    example: `lowkey nums: num[] = range(5);    // [0,1,2,3,4]\nlowkey nums2: num[] = range(2, 6); // [2,3,4,5]`,
    category: "Built-in Functions"
  },
  {
    id: "abs",
    title: "abs",
    aliases: ["absolute", "magnitude"],
    description: "Returns the absolute value of a number.",
    example: `lowley val: num = abs(-42); // 42`,
    category: "Built-in Functions"
  },
  {
    id: "pow",
    title: "pow",
    aliases: ["power", "exponent", "raise"],
    description: "Returns a number raised to the power of another. pow(base, exponent).",
    example: `lowkey result: num = pow(2, 10); // 1024`,
    category: "Built-in Functions"
  },
  {
    id: "sqrt_func",
    title: "sqrt",
    aliases: ["square root", "root"],
    description: "Returns the square root of a number.",
    example: `lowkey val: num = sqrt(144); // 12`,
    category: "Built-in Functions"
  },
  {
    id: "str_func",
    title: "str",
    aliases: ["to string", "convert string", "stringify"],
    description: "Converts a value to a string.",
    example: `lowkey text: txt = str(42); // "42"`,
    category: "Built-in Functions"
  },
  {
    id: "num_func",
    title: "num",
    aliases: ["to number", "convert number", "parse number"],
    description: "Converts a value to a number. Returns 0 if conversion fails.",
    example: `lowley val: num = num("42"); // 42`,
    category: "Built-in Functions"
  },
  {
    id: "input_func",
    title: "input",
    aliases: ["read", "prompt", "user input", "scanf"],
    description: "Reads a line of input from the user. Optionally takes a prompt string.",
    example: `lowkey name: txt = input("What's your name? ");\nspill_tea("Hello " + name);`,
    category: "Built-in Functions"
  },

  // ─── Brainrot Keywords ───────────────────────────────
  {
    id: "tung_tung_tung_sahur",
    title: "tung_tung_tung_sahur",
    aliases: ["wake up", "initialize", "start", "sahur"],
    description: "Time to wake up your code. Prints a wake-up message and initializes execution.",
    example: `tung_tung_tung_sahur;`,
    category: "Brainrot"
  },
  {
    id: "ballerina_cappuccina",
    title: "ballerina_cappuccina",
    aliases: ["fancy exit", "fancy string", "graceful"],
    description: "A graceful and fancy operation. Returns the string \"Fancy Ballerina Cappuccina\".",
    example: `lowkey drink: txt = ballerina_cappuccina();\nspill_tea(drink);`,
    category: "Brainrot"
  },
  {
    id: "skibidi_toilet",
    title: "skibidi_toilet",
    aliases: ["flush", "garbage collection", "clear", "gc"],
    description: "Flushes the memory or triggers garbage collection. Prints a flush message.",
    example: `skibidi_toilet;`,
    category: "Brainrot"
  },
  {
    id: "skibidi",
    title: "skibidi",
    aliases: ["bad", "evil", "chaotic"],
    description: "Something chaotic or evil. Can be used as a variable name or identifier.",
    example: `lowkey x: txt = "skibidi";`,
    category: "Brainrot"
  },
  {
    id: "fanum_tax",
    title: "fanum_tax",
    aliases: ["steal", "subtract", "deduct", "tax"],
    description: "Steals 20% of a variable's value. When called with a variable name, it mutates the variable in-place.",
    example: `lowkey purse: num = 500;\nfanum_tax(purse); // Mutates purse to 400\nspill_tea("Purse after tax:", purse);`,
    category: "Brainrot"
  },
  {
    id: "rizz",
    title: "rizz",
    aliases: ["charisma", "add", "success", "charm", "boost"],
    description: "Adds 10.0 charisma to a variable. When called with a variable name, it mutates the variable in-place.",
    example: `lowkey charm: num = 75;\nrizz(charm); // Mutates charm to 85\nspill_tea("Charm level:", charm);`,
    category: "Brainrot"
  },
  {
    id: "ohio",
    title: "ohio",
    aliases: ["error", "chaotic state", "weird", "runtime error"],
    description: "Triggers a chaotic runtime error. Use it to simulate error conditions.",
    example: `sus (place == "Ohio") {\n    ohio(); // Runtime error!\n}`,
    category: "Brainrot"
  },
  {
    id: "mewing",
    title: "mewing",
    aliases: ["silence", "sleep", "wait", "pause"],
    description: "Pauses execution for a specified number of milliseconds. Defaults to 1000ms (1 second).",
    example: `mewing(2000); // Wait 2 seconds`,
    category: "Brainrot"
  },
  {
    id: "grimace_shake",
    title: "grimace_shake",
    aliases: ["fatal error", "crash", "poison", "throw"],
    description: "Triggers a fatal error crash. Use it to simulate unrecoverable error conditions.",
    example: `sus (critical_failure) {\n    grimace_shake; // Fatal crash!\n}`,
    category: "Brainrot"
  },
  {
    id: "edge",
    title: "edge",
    aliases: ["yield", "almost finish", "pause"],
    description: "Prints a message about edging towards completion. A humorous yield-like statement.",
    example: `edge;`,
    category: "Brainrot"
  }
];